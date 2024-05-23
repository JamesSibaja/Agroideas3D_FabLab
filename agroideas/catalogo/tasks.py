from celery import shared_task
import shutil
from celery.result import AsyncResult
from celery import current_task
import os
import math
# import openslide
from PIL import Image
from catalogo.models import modelo3d

# @shared_task(bind=True)
# def convert_to_tiles(self,input_path, output_path, idOpenSLide, idSlide,tile_size=256):
    
#     try:
        

#         slide = openslide.open_slide(input_path)
#         mpp_x = float(slide.properties[openslide.PROPERTY_NAME_MPP_X])
#         mpp_y = float(slide.properties[openslide.PROPERTY_NAME_MPP_Y])
        

#         slide_width, slide_height = slide.dimensions
#         num_levels = slide.level_count
#         resolution = 1/max(slide_width, slide_height)
#         quotient =  1 -  resolution
        
#         maxlatlng = 90 - math.degrees(math.asin(quotient))
        
#         minZoom = math.ceil(math.log2(90/maxlatlng ))

#         os.makedirs(output_path, exist_ok=True)
#         base_level = math.ceil(math.log(max(slide_width, slide_height) / tile_size, 2))
        
#         total_tiles = pow(pow(2,base_level),2)  
#         self.update_state(state='PROGRESS', meta={'current': 0, 'total': total_tiles})
       
#         pixxm = (40075000/(tile_size * pow(2,minZoom+base_level) ) ) * slide_width
        
#         factor = ((tile_size * pow(2,minZoom+base_level))/40075000) * ((mpp_x + mpp_y)/2)
     
#         if (base_level>num_levels):
#             minZoom = minZoom + base_level - num_levels
#             base_level=num_levels
            
#         slide_widthZ0,slide_heightZ0 = slide.level_dimensions[base_level-1]
#         offsetx = ((slide_width / (math.ceil(slide_widthZ0/ tile_size) * tile_size * slide.level_downsamples[base_level-1])) - 1 ) * (180  /  pow(2, minZoom))
#         offsety = (1 - (slide_height / (math.ceil(slide_heightZ0/ tile_size) * tile_size * slide.level_downsamples[base_level-1]))) * (90 /  pow(2, minZoom))
#         xy_base_level_folder = pow(2,(minZoom)) - 1
        
        

#         row_folderII = os.path.join(output_path, str(1))
        
#         os.makedirs(row_folderII, exist_ok=True)
#         thumbnail = slide.get_thumbnail((256, 256))
#         tile_filename = os.path.join(row_folderII,f"{0}.jpg")
#         thumbnail.save(tile_filename, "JPEG")
#         for level in range(num_levels):

#             level_width, level_height = slide.level_dimensions[level]
#             level_downsample = slide.level_downsamples[level]
#             num_level_folder = base_level-level
#             level_folder = os.path.join(output_path, str(num_level_folder+minZoom))
#             xy_level_folder = xy_base_level_folder * pow(2,num_level_folder-1)
            
#             if num_level_folder>0:
#                 os.makedirs(level_folder, exist_ok=True)
                
#                 rows = math.ceil(level_height / tile_size)
#                 cols = math.ceil(level_width / tile_size)
#                 print( offsetx)
#                 print( offsety)

#                 for row in range(rows):
#                     row_folder = os.path.join(level_folder, f"{row + xy_level_folder}")
#                     os.makedirs(row_folder, exist_ok=True)
                    
                    
#                     for col in range(cols):
#                         x = col * tile_size * int(level_downsample)
#                         y = row * tile_size * int(level_downsample)
                        
                        
#                         tile = slide.read_region((x, y), level, (tile_size, tile_size))
#                         tile = tile.convert("RGB")  
                        
#                         tile_filename = os.path.join(row_folder, f"{col + xy_level_folder}.jpg")
#                         tile.save(tile_filename, "JPEG")
                        
#                         print(f"Saved: {tile_filename}")
#                 print(f"row: {row}")
        
#         rawSlide = OpenSlide.objects.get(id=idOpenSLide)
#         catalogoSlide = modelo3d.objects.get(id=idSlide)
#         rawSlide.assembled = True
#         catalogoSlide.assembled = True
#         catalogoSlide.zoomM = base_level + minZoom
#         catalogoSlide.zoomI = minZoom + 2
#         catalogoSlide.zoomMin = minZoom + 1
#         catalogoSlide.centerLat = offsety
#         catalogoSlide.centerLng = offsetx
#         catalogoSlide.maxLatLng = 2 * maxlatlng
#         catalogoSlide.factor = factor
#         rawSlide.save()
#         catalogoSlide.save()
#         print(total_tiles)
#         slide.close()
        
#         return base_level
#     except Exception as e:
#         try:
#             shutil.rmtree(output_path)
#         except:
#             print("Directorio no existe")
        
#         os.remove(input_path)
#         catalogoSlide = modelo3d.objects.get(id=idSlide)
#         catalogoSlide.error = True
#         catalogoSlide.save()
#         print(f"An error occurred: {str(e)}")
#         return f"Error: {str(e)}"