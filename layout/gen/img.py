import klayout.lay as lay, sys
v = lay.LayoutView(); v.load_layout(sys.argv[1], True); v.max_hier()
try: v.load_layer_props('/foss/pdks/sky130A/libs.tech/klayout/tech/sky130A.lyp')
except Exception as e: print('lyp', e)
v.zoom_fit(); v.save_image(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
