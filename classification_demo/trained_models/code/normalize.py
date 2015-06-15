from PIL import Image, ImageOps, ImageFilter
import PIL

def _is_within(pixel):
    '''
        Check that pixel's rgb components are withing certrain threshold
    '''
    value = 255
    percent = 0.2
    threshold = value * percent
    if (pixel[0] <= threshold) and (pixel[1] <= threshold) and (pixel[2] <= threshold):
        return True
    return False

def normalize(img_path):
    '''
    Make background black, and digit white.
    :param img_path:
    :return:
    '''
    # TODO remove single pixel outliers
    digit_color = (255, 255, 255, 255)
    bg_color = (0, 0, 0, 255)
    img = Image.open(img_path)
    pix_data = img.load()
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if _is_within(pix_data[x, y]):
                pix_data[x, y] = bg_color
            else:
                pix_data[x, y] = digit_color
                try:
                    pix_data[x-1, y] = digit_color # top
                except Exception:
                    pass

    new_width = 130
    new_height = 130
    width, height = img.size
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    img = img.crop((left, top, right, bottom))
    if img.size != (28, 28):
        # img = ImageOps.fit(img, (28, 28), Image.ANTIALIAS)
        img = img.resize((28, 28), PIL.Image.ANTIALIAS)
    return img

if __name__ == "__main__":
    img = normalize('/home/aseke/research/theano/classification_demo/uploads/two.png')
    img.filter(ImageFilter.FIND_EDGES)
    img.show()
    img.save('/home/aseke/research/theano/classification_demo/uploads/one_processed.png')