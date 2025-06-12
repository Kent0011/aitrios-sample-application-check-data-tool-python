import os
import sys
import base64
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from SmartCamera import ObjectDetectionTop
from SmartCamera import BoundingBox
from SmartCamera import BoundingBox2d

if __name__ == '__main__':

    inference_dir = './Inferences'
    # Process all inference result files in the inference_dir
    for inf_file in os.listdir(inference_dir) :
        inf_path = './{0}/{1}'.format(inference_dir,inf_file)
        # Read one file in the folder.
        with open(inf_path, 'r', encoding='utf-8') as json_file:
            buf = json.load(json_file)
        # Base64 decode the string in the file.
        if 'O' in buf['Inferences'][0]:
            buf_decode = base64.b64decode(buf['Inferences'][0]['O'])
        else:
            with open('decoded_result_ObjectDetection.json', 'w', encoding='utf-8') as file:
                json.dump(buf, file, ensure_ascii=False, indent=4)
        # Deserialize the Base64-decoded string.
        ppl_out = ObjectDetectionTop.ObjectDetectionTop.GetRootAsObjectDetectionTop(buf_decode, 0)
        obj_data = ppl_out.Perception()
        res_num = obj_data.ObjectDetectionListLength()
        # Store the deserialized data in json format.
        buf['Inferences'][0].pop('O')
        for i in range(res_num):
            obj_list = obj_data.ObjectDetectionList(i)
            union_type = obj_list.BoundingBoxType()
            if union_type == BoundingBox.BoundingBox.BoundingBox2d:
                bbox_2d = BoundingBox2d.BoundingBox2d()
                bbox_2d.Init(obj_list.BoundingBox().Bytes, obj_list.BoundingBox().Pos)
                buf['Inferences'][0][str(i + 1)] = {}
                buf['Inferences'][0][str(i + 1)]['C'] = obj_list.ClassId()
                buf['Inferences'][0][str(i + 1)]['P'] = obj_list.Score()
                buf['Inferences'][0][str(i + 1)]['X'] = bbox_2d.Left()
                buf['Inferences'][0][str(i + 1)]['Y'] = bbox_2d.Top()
                buf['Inferences'][0][str(i + 1)]['x'] = bbox_2d.Right()
                buf['Inferences'][0][str(i + 1)]['y'] = bbox_2d.Bottom()
        # Output a json file.
        with open('./{0}/decoded_{1}'.format(inference_dir,inf_file), 'w', encoding='utf-8') as file:
            json.dump(buf, file, ensure_ascii=False, indent=4)