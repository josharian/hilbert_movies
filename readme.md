What
----

Convert a movie into an image by treating it as a 3d block, walking it with a space-filling 3d curve, and rendering the results with a space-filling 2d curve.

Inspired by:

  * [Portrait of the Hilbert curve](http://corte.si/posts/code/hilbert/portrait/index.html) and other awesome blog posts and code by Aldo Cortesi
  * [Movie barcode](http://moviebarcode.tumblr.com/)
  * @burnto's birthday

Setup
-----

    pip install -r requirements.txt

Make a pretty picture
---------------------

First, preprocess a movie into frames:

    ./preprocess.sh ~/lorax_trailer.mov ~/lorax_trailer_frames

Then turn the frames into a picture:

    # Fast
    ./process.py --size 512 ~/lorax_trailer_frames hilbert_lorax_fast.png

    # Medium
    ./process.py --size 1024 ~/lorax_trailer_frames hilbert_lorax_medium.png

    # Best quality
    ./process.py --size 4096 ~/lorax_trailer_frames hilbert_lorax_best.png

    # Different "map" and "colorsource" options
    ./process.py --size 1024 --colorsource gray --map hcurve ~/lorax_trailer_frames hilbert_lorax_best.png

    # Try *all* the options! Some of them will fail, but so what...
    for c in gray hcurve hilbert natural zigzag zorder
    do
        for m in gray hcurve hilbert natural zigzag zorder
        do
            ./process.py -s 1024 -c $c -m $m hilbert_lorax-c_$c-m_$m-1024.png
        done
    done

