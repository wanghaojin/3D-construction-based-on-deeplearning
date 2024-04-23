from depth_anything.dpt import DepthAnything

encoder = "vits"  # can also be 'vitb' or 'vitl'
depth_anything = DepthAnything.from_pretrained(
    "LiheYoung/depth_anything_{:}14".format(encoder)
)
