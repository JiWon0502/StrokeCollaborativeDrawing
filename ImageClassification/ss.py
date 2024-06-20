import cairo

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 400, 400)
context = cairo.Context(surface)
context.set_line_width(9)
context.move_to(50, 50)
context.line_to(350, 350)
context.stroke()
surface.write_to_png("example.png")
