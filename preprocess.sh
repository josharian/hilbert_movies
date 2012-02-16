#!/bin/bash

if [ -z $1 ]; then
  echo "usage: preprocess.sh <input_movie> <output_dir>"
  exit 1
fi

if [ -z $2 ]; then
  echo "usage: preprocess.sh <input_movie> <output_dir>"
  exit 1
fi

if [ ! -e $1 ]; then
  echo "Couldn't find input movie $1"
  exit 1
fi

if [ -e $2 ]; then
  echo "output directory already exists"
  exit 1
fi

echo "STARTING..."
echo "-----------"

mkdir -p $2
ffmpeg -i $1 -f image2 $2/frame-%07d.png -vsync 0 -vf select="eq(pict_type\,PICT_TYPE_I)"

echo "-----------"
echo "DONE"
echo
echo "Output frames written to $2"
