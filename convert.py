import sys
from toascii import (
    ColorConverter,
    ConverterOptions,
    Video,
    gradients,
)


class ConvertVideo(Video):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, outfile):
        with self.source as video:
            video.ensure_valid()
            frames = list(self._get_ascii_frames(video))
            with open(outfile, "w", encoding="utf-8") as f:
                f.write("\n\n\n".join(frames))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert.py <infile> <outfile>")
        sys.exit()

    options = ConverterOptions(gradient=gradients.LOW, height=15, x_stretch=2)
    converter = ColorConverter(options)
    video = ConvertVideo(sys.argv[1], converter)
    video.save(sys.argv[2])
