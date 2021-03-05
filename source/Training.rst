학습 - 커스텀 데이터셋 만들기
======================================

1. 데이터 분리
--------------------------
Dataset은 훈련(train)과 검증(val)로 나누어진다.
일반적으로 9:1, 7:3의 비율로 나누는데 Labeling한 데이터를 해당 비율에 맞게 나눠주는 코드가 참고한 사이트에서 제공되었다.(https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/training.html)

코드
    .. code-block:: default
        """ usage: partition_dataset.py [-h] [-i IMAGEDIR] [-o OUTPUTDIR] [-r RATIO] [-x]

        Partition dataset of images into training and testing sets

        optional arguments:
          -h, --help            show this help message and exit
          -i IMAGEDIR, --imageDir IMAGEDIR
                                Path to the folder where the image dataset is stored. If not specified, the CWD will be used.
          -o OUTPUTDIR, --outputDir OUTPUTDIR
                                Path to the output folder where the train and test dirs should be created. Defaults to the same directory as IMAGEDIR.
          -r RATIO, --ratio RATIO
                                The ratio of the number of test images over the total number of images. The default is 0.1.
          -x, --xml             Set this flag if you want the xml annotation files to be processed and copied over.
        """

        import os
        import re
        from shutil import copyfile
        import argparse
        import math
        import random


        def iterate_dir(source, dest, ratio, copy_xml):
            source = source.replace('\\', '/')
            dest = dest.replace('\\', '/')
            train_dir = os.path.join(dest, 'train')
            test_dir = os.path.join(dest, 'test')

            if not os.path.exists(train_dir):
                os.makedirs(train_dir)
            if not os.path.exists(test_dir):
                os.makedirs(test_dir)

            images = [f for f in os.listdir(source)
                      if re.search(r'([a-zA-Z0-9\s_\\.\-\(\):])+(.jpg|.jpeg|.png)$', f)]

            num_images = len(images)
            num_test_images = math.ceil(ratio*num_images)

            for i in range(num_test_images):
                idx = random.randint(0, len(images)-1)
                filename = images[idx]
                copyfile(os.path.join(source, filename),
                         os.path.join(test_dir, filename))
                if copy_xml:
                    xml_filename = os.path.splitext(filename)[0]+'.xml'
                    copyfile(os.path.join(source, xml_filename),
                             os.path.join(test_dir,xml_filename))
                images.remove(images[idx])

            for filename in images:
                copyfile(os.path.join(source, filename),
                         os.path.join(train_dir, filename))
                if copy_xml:
                    xml_filename = os.path.splitext(filename)[0]+'.xml'
                    copyfile(os.path.join(source, xml_filename),
                             os.path.join(train_dir, xml_filename))


        def main():

            # Initiate argument parser
            parser = argparse.ArgumentParser(description="Partition dataset of images into training and testing sets",
                                             formatter_class=argparse.RawTextHelpFormatter)
            parser.add_argument(
                '-i', '--imageDir',
                help='Path to the folder where the image dataset is stored. If not specified, the CWD will be used.',
                type=str,
                default=os.getcwd()
            )
            parser.add_argument(
                '-o', '--outputDir',
                help='Path to the output folder where the train and test dirs should be created. '
                     'Defaults to the same directory as IMAGEDIR.',
                type=str,
                default=None
            )
            parser.add_argument(
                '-r', '--ratio',
                help='The ratio of the number of test images over the total number of images. The default is 0.1.',
                default=0.1,
                type=float)
            parser.add_argument(
                '-x', '--xml',
                help='Set this flag if you want the xml annotation files to be processed and copied over.',
                action='store_true'
            )
            args = parser.parse_args()

            if args.outputDir is None:
                args.outputDir = args.imageDir

            # Now we are ready to start the iteration
            iterate_dir(args.imageDir, args.outputDir, args.ratio, args.xml)


        if __name__ == '__main__':
            main()


실행
    .. code-block:: default
        python partition_dataset.py -x -i [PATH_TO_IMAGES_FOLDER] -r 0.1

* 주의할점은 labeling된 xml파일과 이미지 파일은 항상 쌍을 맞춰야하고 label 이름은 추후 작성하게 될 label_map에 작성된 클래스여야 한다.

위 과정까지 끝나면 tutorial을 그대로 따라하는건 여기까지 하고 이제 tensorflow github 공식 문서를 보도록 하자.
공식문서에서 말하는 label map은 key-value형식을 가진다.

예시
    .. code-block:: default
        item {
          id: 1
          display_name: "dog"
        }
        item {
          id: 2
          display_name: "bird"
        }
        item {
          id: 3
          display_name: "cow"
        }

2. 딥러닝 모델 선정
---------------------------
model zoo라는게 있다. 정말 동물원처럼 model을 다 모아둔 곳으로 FPS, mAP등 성능 지표를 보고 구글에서 검색 후 적합한 모델을 선택하여 진행한다.(https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md)


3. 학습(디렉토리 트리 구조)
------------------------------
Google Tensorflow팀에서 추천하는 디렉토리 구조는 다음과 같다.

    .. code-block:: default
        Object_detection
        ├── data/
        │   ├── eval-00000-of-00001.tfrecord
        │   ├── label_map.txt
        │   ├── train-00000-of-00002.tfrecord
        │   └── train-00001-of-00002.tfrecord
        └── models/
            └── my_model_dir/
                ├── eval/                 # Created by evaluation job.
                ├── my_model.config
                └── model_ckpt-100-data@1 #
                └── model_ckpt-100-index  # Created by training job.
                └── checkpoint            #


* object_detection 디렉토리 밑에 있는 data디렉토리에 label map과 tfrecord파일들을 넣어준다.
* 2번에서 선정한 모델을 압축해제하여 models밑에 새로 디렉토리를 생성한 후 그 밑에 압축해제한다. (checkpoint, saved_model디렉토리와 pipeline.config 파일이 존재한다.)
* 이제 pipeline.config파일을 수정해야한다.

4. 학습(pipeline 수정)
-----------------------------
num_classes에 대해서는 label map에 있는 총 클래스 개수를 적어준다.
batch_size는 1로 설정한 후 조금씩 올려가며 해당 gpu 메모리 상황에 맞게 값을 정해준다.
total_steps와 num_steps도 적당히 설정해주어야한다. 적당히라고 하는 이유는 과도하게 설정하는 경우 역전파 과정에서 loss함수에서 오류가 발생해 loss율이 nan이 나올 수 있기 때문이다.
fine_tune_checkpoint는 2번과 3번과정에서 받은 모델의 checkpoint경로를 상대경로로 잡아주어야한다.
예시
fine_tune_checkpoint: "models/yhj_ssd_efficientdet/efficientdet_d2_coco17_tpu-32/checkpoint/ckpt-0"
label_map_path에는 data밑에 있는 label map파일을 설정해준다
input_path에는 각 reader의 타입에 맞게 train.record와 test.record파일의 경로를 잡아준다.
주의할 점은 모든 경로는 상대경로로 작성해야한다.
진짜 이게 좀 어이가 없는게 절대경로로 하면 dead lock걸려서 상대경로로 고치니까 잘된다..

5.학습(진짜 학습)
이제 명령어를 입력해서 정말 학습에 들어가도록한다.
그 전에 위에 개인 model폴더에 temp_ckpt라는 이름이나 뭐 자유롭게 check point 가 저장될 디렉토리를 하나 생성한다.
이후 research 폴더에서 아래 명령어를 실행한다.

--pipeline_config_path에는 조금 전 수정했던 pipline이 존재하는 path를 입력하고 --model_dir에는 조금 전 생성했던 디렉토리의 경로를 잡아준다.
python model_main_tf2.py --pipeline_config_path=./models/yhj_ssd_efficientdet/efficientdet_d2_coco17_tpu-32/pipeline.config --model_dir=./models/yhj_ssd_efficientdet/efficientdet_d2_coco17_tpu-32/ckpt_temp/

6.학습 후 모델 export
이제 학습이 끝났다. 학습된 모델을 사용할 수 있게 export하는 과정이 필요하다.

5번에서 입력한 옵션에 --output_directory는 외부로 export될 파일이 저장될 경로를 입력해준다.
python /PATH/TO/EXPORTER_MAIN_V2.PY_EXIST_DIR/exporter_main_v2.py --input_type image_tensor --pipeline_config_path /PATH/TO/MODEL/PIPLINE_CONFIG_FILE/PATH/pipeline.config --trained_checkpoint_dir /PATH/TO/CREATED/DIRECTORY/FOR/SAVE/CHECKPOINT/ckpt_temp/ --output_directory ./object_detection/models/yhj_ssd_resnet/exported_model/