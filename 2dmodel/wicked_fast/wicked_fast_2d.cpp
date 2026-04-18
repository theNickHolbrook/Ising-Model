// 2D Ising Model
// No external dependencies — uses a hand-written BMP writer.
//
// Compile:
//   g++ -O2 -static -o ising super_fast_2d.cpp
//
// Make video after running:
//   ffmpeg -framerate 30 -i frames/frame_%05d.bmp -c:v libx264 -pix_fmt yuv420p ising.mp4

#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <iostream>

#ifdef _WIN32
  #include <direct.h>
  #include <windows.h>
  #define MAKE_DIR(p) _mkdir(p)
#else
  #include <sys/stat.h>
  #include <unistd.h>
  #define MAKE_DIR(p) mkdir(p, 0755)
#endif

// ── tuneable constants ────────────────────────────────────────────────────────
static const int    LENGTH      = 64;   // lattice side (must be even)
static const int    SCALE       = 8;    // pixels per spin
static const int    SPIN_FLIPS  = 20000; // outer MC steps
static const double TEMP        = 1; // near critical temp (Tc ≈ 2.269)
static const int    FRAME_EVERY = 20;   // save a frame every N steps

// ── minimal BMP writer ────────────────────────────────────────────────────────
// Writes a 24-bit RGB BMP. Returns true on success.
// BMP rows must be padded to a multiple of 4 bytes.
static bool write_bmp(const char* filename, const uint8_t* rgb,
                      int width, int height) {
    int row_bytes   = width * 3;
    int row_padded  = (row_bytes + 3) & ~3;          // round up to 4
    int pixel_bytes = row_padded * height;
    int file_size   = 54 + pixel_bytes;              // 54-byte header

    uint8_t hdr[54];
    memset(hdr, 0, sizeof(hdr));

    // BMP file header (14 bytes)
    hdr[0] = 'B'; hdr[1] = 'M';
    hdr[2] = file_size & 0xFF;
    hdr[3] = (file_size >> 8)  & 0xFF;
    hdr[4] = (file_size >> 16) & 0xFF;
    hdr[5] = (file_size >> 24) & 0xFF;
    hdr[10] = 54; // pixel data offset

    // DIB header (40 bytes, BITMAPINFOHEADER)
    hdr[14] = 40;  // header size
    hdr[18] = width  & 0xFF;
    hdr[19] = (width  >> 8) & 0xFF;
    hdr[22] = height & 0xFF;         // positive = bottom-up
    hdr[23] = (height >> 8) & 0xFF;
    hdr[26] = 1;   // color planes
    hdr[28] = 24;  // bits per pixel

    FILE* f = fopen(filename, "wb");
    if (!f) {
        std::cerr << "ERROR: cannot open \"" << filename << "\" for writing\n";
        return false;
    }
    fwrite(hdr, 1, 54, f);

    // BMP stores rows bottom-up and channels as BGR
    uint8_t* row = new uint8_t[row_padded];
    memset(row, 0, row_padded);
    for (int j = height - 1; j >= 0; --j) {   // bottom-up
        for (int i = 0; i < width; ++i) {
            int src  = (j * width + i) * 3;
            int dst  = i * 3;
            row[dst + 0] = rgb[src + 2]; // B
            row[dst + 1] = rgb[src + 1]; // G
            row[dst + 2] = rgb[src + 0]; // R
        }
        fwrite(row, 1, row_padded, f);
    }
    delete[] row;
    fclose(f);
    return true;
}

// ─────────────────────────────────────────────────────────────────────────────
class Lattice {
public:
    Lattice() { initialize(); }

    void initialize() {
        for (int j = 0; j < LENGTH; ++j)
            for (int i = 0; i < LENGTH; ++i)
                arr[j][i] = (rand() > RAND_MAX / 2) ? 1 : -1;
    }

    void metropolis(int i, int j, double temp) {
        int dE = delta_E(i, j);
        if (dE < 0) {
            arr[j][i] = -arr[j][i];
        }else if ((dE != 0) && ((double)rand() / RAND_MAX) < std::exp(-dE / temp)) {
            arr[j][i] = -arr[j][i];
        }
    }

    bool write_frame(const char* filename) const {
        const int W   = LENGTH * SCALE;
        const int H   = LENGTH * SCALE;
        const int BUF = W * H * 3;

        uint8_t* img = new (std::nothrow) uint8_t[BUF];
        if (!img) {
            std::cerr << "ERROR: out of memory allocating frame buffer\n";
            return false;
        }

        for (int j = 0; j < LENGTH; ++j) {
            for (int i = 0; i < LENGTH; ++i) {
                uint8_t c = (arr[j][i] == 1) ? 255 : 0;
                for (int py = 0; py < SCALE; ++py) {
                    for (int px = 0; px < SCALE; ++px) {
                        int base = ((j * SCALE + py) * W + (i * SCALE + px)) * 3;
                        img[base + 0] = c;
                        img[base + 1] = c;
                        img[base + 2] = c;
                    }
                }
            }
        }

        bool ok = write_bmp(filename, img, W, H);
        delete[] img;
        return ok;
    }

private:
    signed char arr[LENGTH][LENGTH];

    int delta_E(int i, int j) const {
        int s     = arr[j][i];
        int up    = arr[(j == 0)          ? LENGTH - 1 : j - 1][i];
        int down  = arr[(j == LENGTH - 1) ? 0          : j + 1][i];
        int left  = arr[j][(i == 0)          ? LENGTH - 1 : i - 1];
        int right = arr[j][(i == LENGTH - 1) ? 0          : i + 1];
        return 2 * s * (up + down + left + right);
    }
};

// ─────────────────────────────────────────────────────────────────────────────
int main() {
    srand(static_cast<unsigned>(time(0)));

    MAKE_DIR("frames");

    {
        char cwd[512] = {};
#ifdef _WIN32
        GetCurrentDirectoryA(sizeof(cwd), cwd);
#else
        if (!getcwd(cwd, sizeof(cwd))) { cwd[0]='.'; cwd[1]='\0'; }
#endif
        std::cout << "Working directory : " << cwd << "\n";
        std::cout << "Frames location   : " << cwd << "\\frames\\\n";
        std::cout << "Total frames      : " << (SPIN_FLIPS / FRAME_EVERY) << "\n\n";
        std::cout.flush();
    }

    Lattice lattice;
    int frame_idx = 0;
    char path[256];

    for (int step = 0; step < SPIN_FLIPS; ++step) {

        // Red squares: i+j even
        for (int j = 0; j < LENGTH; ++j)
            for (int i = (j & 1); i < LENGTH; i += 2)
                lattice.metropolis(i, j, TEMP);

        // Black squares: i+j odd
        for (int j = 0; j < LENGTH; ++j)
            for (int i = 1 - (j & 1); i < LENGTH; i += 2)
                lattice.metropolis(i, j, TEMP);

        if (step % FRAME_EVERY == 0) {
            snprintf(path, sizeof(path), "frames/frame_%05d.bmp", frame_idx);
            if (lattice.write_frame(path)) {
                std::cout << "wrote " << path << "\n";
                std::cout.flush();
                ++frame_idx;
            } else {
                std::cerr << "Aborting — frame write failed.\n";
                return 1;
            }
        }
    }

    std::cout << "\nDone. " << frame_idx << " frames in frames/\n\n"
              << "Compile video:\n"
              << "  ffmpeg -framerate 30 -i frames/frame_%05d.bmp"
                 " -c:v libx264 -pix_fmt yuv420p ising.mp4\n\n";

#ifdef _WIN32
    std::cout << "Press Enter to exit...\n";
    std::cin.get();
#endif
    return 0;
}