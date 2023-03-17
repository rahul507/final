
import argparse
import io
import os
from PIL import Image
import datetime

import torch
from flask import Flask, render_template, request, redirect
img_bytes = file.read()
img = Image.open(io.BytesIO(img_bytes))