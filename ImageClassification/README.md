# Stroke-based Collaborative Drawing between AI and Human

Stroke-based Collaborative Drawing between AI and Human


## Installation
Implemented using python==3.9.*

Get the Source Code
 - Download Zip file from " https://github.com/JiWon0502/StrokeCollaborativeDrawing "
 - Unzip the file to "StrokeCollaborativeDrawing-main" folder

Get seed.npy(153M) file (https://github.com/CMACH508/Lmser-pix2seq - Preparing Dataset)
 - Download random mask seed file from https://drive.google.com/file/d/1Q_LTd174AKEOi4zA3ff1Aa3j6qAR7kr8/view
 - Move to StrokeCollaborativeDrawing-main/lmser/utils

Set Python Virtual Environment
 - modify conda_requirements.yaml file
	1. name: vLmser -> name: YourVenvName
	2. prefix: /Users/userID/opt/anaconda3/envs/vLmser -> prefix: /path/conda_env/YourVenvName

 - run
```bash
cd path/to/StrokeCollaborativeDrawing-main
conda env create -f conda_requirements.yaml
conda activate vSCD
```

## Run the program

```shell
python demoUI.py
```

## Code Explanation

### [UI]

#### demoUI.py
: 메인 함수로, painter 객체와 파일들을 접근하고 메소드를 부르는 역할이다.

painter = MousePainter()
: MousePainter 클래스의 객체를 선언한다.

painter.current_frame_index == 0 
: AI가 완료된 이후 그림을 그리는 단계
: AI 모델이 저장한 Npy 파일의 데이터를 불러와  캔버스를 업데이트 하고, 마우스 입력을 받는다.

painter.current_frame_index == 1
: RDP algorithm을 사용해 마지막으로 저장된 Npy 파일의 데이터를 전처리하고, 전처리 된 데이터를 이용하여 캔버스를 업데이트 한다.

painter.current_frame_index == 2
: AI 모델을 사용하기 위해 stroke.run 메소드를 실행한다. 획이 추가된 데이터가 Npz 파일 형태이므로 이를 Npy형태로 다시 저장한 뒤, Npy 데이터를 이용하여 캔버스를 업데이트 한다.

#### MousePainter class
: 모든 인터페이스(canvas, button) 등을 구현한 클래스이다.

load_and_reconstruct(filename = ‘mouse_deltas.npy’)
: npy 파일의 이름을 받아서 저장된 파일이 있는지 확인하고, 저장된 파일에서 데이터를 읽어온 뒤 프레임에 그림으로 그린다.

paint(event), start_paint(event), stop_paint(event)
: 사용자가 그림을 그릴 차례일 때, 마우스가 눌리는 경우 start_paint, 이동하는 경우 paint, 그리고 누른 것을 떼는 경우 stop_paint가 실행된다. 그림을 그리고, (delta_x, delta_y, penstate) 상태의 행렬 데이터를 저장한다.

save_deltas_button(), erase_button(), next_button(), save_button(), exit_button()
: 각 버튼이 눌렸을 때 각자의 기능을 수행한다. save_deltas_button의 경우, 사용자가 그린 그림이 저장된 배열을 npy파일로 저장한다. erase_button의 경우, 그려진 그림을 지움과 동시에 기존의 배열도 초기화한다. next_button은 다음 단계로 넘어가는 역할이다. save_button을 누르면 현재 각 단계에서 마지막으로 저장된 파일들을 다른 폴더에 인덱스와 함께 저장한다. exit_button을 누르면 모든 과정을 마무리하고 프로그램을 종료한다.

### [Lmser-pix2seq] [1]
#### encoder.py
myencoder(nn.Module) 클래스: Lmser Block Encoder을 구현한 클래스로 입력된 numpy.ndarray 타입의 다차원 배열을 latent vector z로 압축한다.

#### decoder.py
DecoderRNN(nn.Module) 클래스: RNN Decoder를 구현한 클래스로 encoder.py로부터 전달받은 latent vector z를 원래의 형태로 복원함으로써 Image Completion을 수행한다.

#### hyper_params.py
HParams 클래스 : Image Completion 관련 매개변수를 초기화한다.

#### inference.py 
: Lmser pix2seq의 메인 파일이며 관련된 파일들로부터 클래스와 함수를 불러오고 이를 기반으로 Image Completion을 수행한다.

Model class : AutoEncoder를 구현한 클래스로 Lmser Block Encoder와 RNN Decoder로 구성된다.

conditional_generation(self, sketch_dataset, save_middle_path="visualize"): Image Completion의 결과인 (dx, dy, pen_state) 형식의 다차원 배열을 .npz 파일에 저장한다.

### [Stroke Ordering]
### stroke.py
Line 클래스 : Start Point인 p1(x1, y1)과 End Point인 p2(x2, y2)를 멤버로 갖고 있는 구조체이다.

find_nearest_strokes (input, result, stroke_n) : Lmser pix2seq를 통해 새롭게 추가된 획 중 stroke_n개를 선택하여 순서를 재정렬한다. 이때, input은 Lmser pix2seq에 입력한 미완성된 그림이며 result는 Lmser pix2seq에 input을 입력하였을 때의 결과이다.

find_nearest_point (line, coord): Line 객체인 line의 Start Point와 End Point 중 coord과 더 가까이 위치한 점을 찾아낸다. 이때, coord는 마지막으로 입력된 획의 End Point이다.

calculate_distance (p1, p2) : p1(x1, y1)과 p2(x2, y2) 사이의 유클리드 거리를 계산 및 반환한다.

xy2line(cumsum) : (x, y, pen_state)로 구성된 다차원 배열을 Line 객체 배열로 변환한다.

line2xy(lines) : Line 객체 배열을 (x, y, pen_state)로 구성된 다차원 배열로 변환한다.


## References

1. **Image Completion Model (Lmser-pix2seq)**: A method for learning stable sketch representations for sketch healing. For more details, refer to the following publication:

   - Li, Tengjie, Sicong Zang, Shikui Tu, and Lei Xu. "Lmser-pix2seq: Learning stable sketch representations for sketch healing." *Computer Vision and Image Understanding* (2024): 103931. [Link to paper](link_to_paper)
  

2. **Image Simplification (RDP)**: This technique utilizes the Ramer-Douglas-Peucker algorithm for image simplification. The software is available at:

   - Hügel, S. (2021). Simplification (Version X.Y.Z) [Computer software]. [Link to software](https://github.com/urschrei/simplification). DOI: [10.5281/zenodo.5774852](https://doi.org/10.5281/zenodo.5774852).
