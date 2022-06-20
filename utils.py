import cv2
import pandas as pd
import cv2
import numpy as np

def format_response(r):
    df = pd.DataFrame(columns = ['label','boundingBox','score','text'])
    for i in r['result'][0]['prediction']:
        df.loc[len(df.index)] = [i['label'],[i['xmin'],i['ymin'],i['xmax'],i['ymax']],round(i['score'],4),str(i['ocr_text'])]
    return df

def write_bbox_image(img_file_in, df):
    img_array = np.array(img_file_in)
    for bbox,det_class in zip(df.boundingBox.to_list(),df['label'].to_list()):
        cv2.rectangle(img_array, (bbox[0], bbox[1]), (bbox[2],bbox[3]), (255, 0, 0), 2)
        cv2.putText(img_array, det_class, (bbox[0]-15,bbox[1]), fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.75, color = (255, 0, 0), thickness = 2)
    # filename = 'out_image.jpg'
    # cv2.imwrite(filename, img_array)
    return img_array