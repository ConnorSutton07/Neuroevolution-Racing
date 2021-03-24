import pygame

def tile_texture(texture, size):
    result = pygame.Surface(size, depth=32)
    for x in range(0, size[0], texture.get_width()):
        for y in range(0, size[1], texture.get_height()):
            result.blit(texture,(x,y))
    return result


def apply_alpha(texture, mask):
    """
    Image should be  a 24 or 32bit image,
    mask should be an 8 bit image with the alpha
    channel to be applied
    """
    texture = texture.convert_alpha()
    target = pygame.surfarray.pixels_alpha(texture)
    target[:] = pygame.surfarray.array2d(mask)
    # surfarray objets usually lock the Surface. 
    # it is a good idea to dispose of them explicitly
    # as soon as the work is done.
    del target
    return texture

def stamp(image, texture, mask, pos):
    image.blit(apply_alpha(texture, mask), pos)

def blit_textured_shape(screen, texture_path: str, blit_pos: tuple, mask: pygame.Surface) -> None:
    texture = tile_texture(pygame.image.load(texture_path), mask.get_size())
    stamp(screen, texture, mask, blit_pos)
