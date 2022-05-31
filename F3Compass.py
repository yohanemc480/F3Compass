#F3の座標の正方向情報のみを表示するロードストーンコンパスに必要なリソース(モデル、テクスチャ)を生成する。

AngleMaxNum = 36#テクスチャ・モデルの通し番号の最大値

from BasicDef import Read, Write, Indention, PathBase
import cv2

BaseImage = cv2.imread(PathBase + 'Resources/f3_compass/f3_compass.png',-1)
Height, Width = BaseImage.shape[0], BaseImage.shape[1]
RotateCenter = (int(Width/2),int(Height/2))

AngleModule = 360/AngleMaxNum

def Make1Texture(AngleNum):#一つの回転角(通し番号)に対応したテクスチャを生成する。
  RotateAngle = - AngleModule * AngleNum
  TransMat = cv2.getRotationMatrix2D(RotateCenter, RotateAngle, 1)
  RotatedImage = cv2.warpAffine(BaseImage, TransMat, (Width, Height))
  cv2.imwrite(PathBase + 'assets/minecraft/textures/item/f3_compass/' + str(AngleNum) + '.png',RotatedImage)

def MakeAllTexture():#全てのテクスチャを生成する。
  for i in range(AngleMaxNum):
    Make1Texture(i)

def Make1Model(AngleNum):#一つの回転角(通し番号)に対応したモデルを生成する
  ModelTemprate = Read('Resources/f3_compass/1ModelHandHeld.txt')
  Content = ModelTemprate.replace('番号',str(AngleNum))
  Write(Content,'assets/minecraft/models/item/f3_compass/' + str(AngleNum) + '.json')

def MakeAllModel():#全てのモデルを生成する
  for i in range(AngleMaxNum):
    Make1Model(i)

def MakeCustomModel():#カスタムモデルデータと元のデータを包含したcompass.jsonを作成する。
  CustomModel = Read('Resources/f3_compass/CustomModel.txt')
  OverrideModule = Read('Resources/f3_compass/OverrideModule.txt')
  OriginalOverride = Read('Resources/f3_compass/OriginalCompassOverride.txt')

  OverrideArray = []
  OverrideArray.append(OriginalOverride)
  for i in range(AngleMaxNum):
    AngleStrNum = 8
    FloatAngle = str(i/AngleMaxNum)[:AngleStrNum]
    FloatAngle = FloatAngle + '0' * (AngleStrNum - len(FloatAngle))
    Element = OverrideModule.replace('角度',FloatAngle).replace('モデル番号',str(i))
    OverrideArray.append(Element)
  Overrides = (',' + Indention) .join (OverrideArray)
  Content = CustomModel.replace('オーバーライド',Overrides)
  Write(Content,'assets/minecraft/models/item/compass.json')

#実行ファイル
MakeAllTexture()
MakeAllModel()
MakeCustomModel()