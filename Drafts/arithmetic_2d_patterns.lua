function pattern(height, width, color_multiplier, shape_multiplier, shapes, colors, cell_style)
   local height = height or 20
   local width = width or 60
   local color_multiplier = color_multiplier or 1
   local shape_multiplier = shape_multiplier or 1
   local shapes = shapes or {"#", "·", "@", "%", "+"}
   local colors = colors or {"\x1b[41m", "\x1b[42m", "\x1b[43m", "\x1b[44m", "\x1b[45m"}
   local reset = "\x1b[0m"
   local cell_style = cell_style or ""
   local str = ""
   for row=0,height do
      for column=0,width do
	 local color_shift = row % #colors
	 local shape_shift = column % #shapes
	 str = str .. (
	    cell_style ..
	    colors[(column + color_multiplier * color_shift) % #colors +1] ..
	    shapes[(row + shape_multiplier * shape_shift) % #shapes +1] ..
	    reset)
      end
      str = str .. "\n"
   end
   return str
end

print(pattern(10,10,0,0))
