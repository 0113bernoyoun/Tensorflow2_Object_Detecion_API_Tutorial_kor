설치
======================================


1. Tensorflow2 Object Detection API 설치하기
--------------------------

Tensorflow Object Detection API의 models repository에서 제공해주는 파일의 구조는 다음과 같습니다.

    .. code-block:: default

        TensorFlow/
        └─ models/
           ├─ community/
           ├─ official/
           ├─ orbit/
           ├─ research/
           └── ...


우선 아래 명령어를 통해 models repository를 clone합니다.
    .. code-block:: default

        git clone https://github.com/tensorflow/models

2. protobuf 설치
--------------------------
제가 처음 참조했던 사이트인 (https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/) 에서는 제가 실수한 부분이 있을 수 있겠지만 protobuf가 정상적으로 동작하지 않았습니다. 그래서 tensorflow1 으로 object detection API를 사용할 때 설치했던 버전으로 진행했습니다.

다음 사이트에 있는 zip파일을 다운받습니다.
(https://github.com/google/protobuf/releases/download/v3.3.0/protoc-3.3.0-linux-x86_64.zip)

* 받은 파일을 적절한 곳에 디렉토리를 만들고 압축을 풀어줍니다.
* 터미널에서 현재 위치를 models 밑에 research 디렉토리로 이동합니다.
* 위에서 압축해제한 proto 디렉토리의 bin까지의 경로를 기억합니다.
* 다음 명령어를 입력해서 에러가 나오지 않는다면 성공입니다.
    .. code-block:: default

         PATH/TO/PROTO/bin/protoc object_detection/protos/*.proto --python_out=.



4. COCO API 설치
--------------------------
처음에 저는 이런 생각이 들었습니다.
내가 COCO API안쓸건데 왜 이걸 설치해야 할까
하지만 반드시 설치해야 합니다.

아래 명령어를 입력해서 cocoapi repository를 clone합니다.
    .. code-block:: default

         git clone https://github.com/cocodataset/cocoapi.git

터미널의 위치를 clone된 디렉토리의 cocoapi/PythonAPI 까지 이동합니다.
이후 make를 입력해 cocoapi를 빌드합니다.
    .. code-block:: default

         make
빌드 후 생성된 pycocotools를 research디렉토리로 복사합니다.
    .. code-block:: default

        cp -r pycocotools PATH/TO/TENSORFLOW/models/research/      // (-r 은 해당 파일 혹은 디렉토리가 외부에서 접근중이여도 복사를 할 수 있게 해주는 옵션)

5. Object Detection API 설치
--------------------------

이 부분이 지금 문서를 작성하면서 가장 애매한 부분입니다.
제가 지금 권장하는 환경과 무언가 달라서 그럴 수 있겠는데 setup.py를 수행하는 순간 파일이 깨지는 현상이 발생했고 복구도 되지 않았습니다.
그래서 다시 처음부터 세팅 후 setup.py를 수행하지 않고 진행했는데 현재 잘 사용하고 있습니다.
이 부분에 대해서 이유를 아신다면 알려주세요.

6. 테스트
--------------------------
google의 tensorflow팀은 친절하게도 정상적으로 설치가 되었는지 테스트를 할 수 있는 파일을 제공해줍니다.
     .. code-block:: default

        python object_detection/builders/model_builder_tf2_test.py

해당 테스트에서 일부 파일이 없다고 말하는 경우가 있을텐데 아래 2개의 명령어를 입력해 환경변수를 잡아준 후 그래도 요구하는건 pip install로 설치를 하면 됩니다.(해당 터미널이나 서버를 재부팅할때마다 환경을 새로 잡으라고 요구할텐데 batch파일로 하나 만들어두는게 편합니다.)
    .. code-block:: default

        export PYTHONPATH=$PYTHONPATH:PATH/TO/TENSORFLOW/models/research:PATH/TO/TENSORFLOW/models/research/slim
        export PYTHONPATH=$PYTHONPATH:PATH/TO/TENSORFLOW/models/

배치 파일을 만드는 방법은 nano나 gedit이나 vim 등을 이용해서 파일을 하나 만든 다음 가장 위에 아래 예약어를 붙여줍니다.
    .. code-block:: default

        #!/bin/bash
배치파일의 실행은 . 명령어로 실행하면 됩니다.
    .. code-block:: default

        ex). set_path.sh

환경변수를 잡으라고 하는 경우는 다음 모듈을 못찾겠다고 하는 경우입니다. (정확히 어떤 것들인지는 잘 기억이 나지 않으나 해당 디렉토리 밑에 있는 파일들을 참조할 때 입니다. 그떄 그때 구글링을 추천드립니다..)
object_detection, slim ...

테스트가 잘 끝나면 아래와 비슷하게 나옵니다.

    .. code-block:: default

        ...
        [       OK ] ModelBuilderTF2Test.test_create_ssd_models_from_config
        [ RUN      ] ModelBuilderTF2Test.test_invalid_faster_rcnn_batchnorm_update
        [       OK ] ModelBuilderTF2Test.test_invalid_faster_rcnn_batchnorm_update
        [ RUN      ] ModelBuilderTF2Test.test_invalid_first_stage_nms_iou_threshold
        [       OK ] ModelBuilderTF2Test.test_invalid_first_stage_nms_iou_threshold
        [ RUN      ] ModelBuilderTF2Test.test_invalid_model_config_proto
        [       OK ] ModelBuilderTF2Test.test_invalid_model_config_proto
        [ RUN      ] ModelBuilderTF2Test.test_invalid_second_stage_batch_size
        [       OK ] ModelBuilderTF2Test.test_invalid_second_stage_batch_size
        [ RUN      ] ModelBuilderTF2Test.test_session
        [  SKIPPED ] ModelBuilderTF2Test.test_session
        [ RUN      ] ModelBuilderTF2Test.test_unknown_faster_rcnn_feature_extractor
        [       OK ] ModelBuilderTF2Test.test_unknown_faster_rcnn_feature_extractor
        [ RUN      ] ModelBuilderTF2Test.test_unknown_meta_architecture
        [       OK ] ModelBuilderTF2Test.test_unknown_meta_architecture
        [ RUN      ] ModelBuilderTF2Test.test_unknown_ssd_feature_extractor
        [       OK ] ModelBuilderTF2Test.test_unknown_ssd_feature_extractor ----------------------------------------------------------------------
        Ran 20 tests in 68.510s
        OK (skipped=1)