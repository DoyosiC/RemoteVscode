#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>

#define MAX_READCHAR 255
#define MAX_DATANUM  1000
#define EPOCH  10
#define MAX_ELEMENTS 100

void Shuffle_Data(double data[][4], int teacher[], int datanum);

// 各層のユニットの値
typedef struct{
  int n;  // ユニット数
  double unit[MAX_ELEMENTS]; // 各ユニットの値
}layer_r;

// 第1層から第2層への重み行列
typedef struct{
  int m;  // 第1層のユニット数
  int n;  // 第2層のユニット数
  double data[MAX_ELEMENTS][MAX_ELEMENTS];  // 重み行列
}weight_r;


/*********************************************************************/
/* 関数MultiplyMatrix：重み行列と入力ベクトルの積を計算する関数 */
/* 入力1：重み行列src1                                     */
/* 入力2：入力ベクトルsrc2                                 */
/* 出力：出力ベクトルdst                                   */
/*********************************************************************/
int MultiplyMatrix(weight_r src1, layer_r src2, layer_r *dst){
  // 関数の中身を記入してください
  // 掛け算ができない場合（要素数の不一致）、-1を返してください
  // 掛け算ができた場合は1を返してください
  if ( src1.m != src2.n || src1.n != dst->n ){
    printf("Multiply Matrix Error\n");
    return -1;
  }
  for ( int i = 0; i < dst->n; i++ ){
    dst->unit[i] = 0.0;
  }
  for ( int i = 0; i < dst->n; i++ ){
    for ( int j = 0; j < src2.n; j++ ){
      dst->unit[i] += src1.data[i][j] * src2.unit[j];   
    }
  }
  return 1;
}

/***************************************************/
/* 関数Step：Step関数を層に適用する関数         */
/* 入力：input    出力：output              */
/***************************************************/
void Step(layer_r input, layer_r *output){
  /*****************************************/
  /* Step関数の中身を以下に記述しなさい */
  /*****************************************/
  if(input.unit[0] > 0){
    output->unit[0] =  1;
  }else{
    output->unit[0] = 0;
  }
}

int main (void){
  layer_r input_l, output_l, step_output_l;
  weight_r weights;
  int loss;

  srand((unsigned)time(NULL));

  FILE *fp;
  char buf[255];
  double data[MAX_DATANUM][4];    // 入力データベクトル
  int teacher[MAX_DATANUM];       // 学習データのラベル（教師データ）
  int datanum = 0;    // データの個数
  
  // アヤメのデータを読み込む
  fp = fopen("iris-class.data", "r");
  while(fgets(buf,MAX_READCHAR,fp) != NULL ){
    sscanf(buf, "%lf,%lf,%lf,%lf,%s", &data[datanum][0],
      &data[datanum][1], &data[datanum][2], &data[datanum][3],
      buf);
    if (strcmp(buf, "Iris-setosa") == 0 ){
      teacher[datanum] = 0;   // 出力 0 とする
     }
    else if ( strcmp(buf, "Iris-versicolor") == 0 ){
      teacher[datanum] = 1;   // 出力 1 とする
     }
    datanum++;
  }
  fclose(fp);
  
  datanum--;
  
  Shuffle_Data(data, teacher, datanum);
  
  input_l.n = 4;
  output_l.n = 1;
  
  weights.m = 4;
  weights.n = 1;
  
  // 重みの初期化
  for ( int j = 0; j < weights.m; j++ ){
    for ( int i = 0; i < weights.n; i++ ){
      weights.data[i][j] = 0.1 * i + 0.1 * j;
     }
   }
 
  for ( int i = 0; i < EPOCH; i++ ){
    loss = 0;
    for ( int j = 0; j < datanum; j++ ){
        /******************************************************/
        /* 入力ベクトルから出力を計算する処理を記述しなさい */
        /* 出力output_lにステップ関数を掛けたものを        */
       /* step_output_lとすること                       */
       /*******************************************************/
       MultiplyMatrix(weights,input_l,&output_l);
       layer_r u;
       for (int i=1;i<output_l.n;i++){
        u.unit[0] += output_l.unit[i];
       }
       u.unit[0] = u.unit[0] - output_l.unit[0];
       Step(u,&step_output_l);

      /********************************************************/
     /* step_output_l.unit[0]とteacher[j]が異なる   */
      /* とき、重みを更新し、lossの値を1増加する処理を     */
      /* 記述しなさい                                        */
      /*******************************************************/
      if(step_output_l.unit[0] != teacher[j]){
        for(int i=0;i < output_l.n ;i++){
          input_l.unit[i] = input_l.unit[i]+(teacher[i]-step_output_l.unit[0]) *input_l.unit[i];
        }
        loss += 1;
      }
     }
    printf("Epoch %d: Loss %d\n", i, loss);
    if ( loss == 0 ){
      break;
     }
   }
 
  return 0;
}

void Shuffle_Data(double data[MAX_DATANUM][4], int teacher[MAX_DATANUM], int datanum){
  double temp_data;
  int temp_teacher;
  for ( int i = datanum-1; i > 0; i-- ){
    int j = rand() % (i + 1);
    for ( int k = 0; k < 4; k++ ){
      temp_data = data[i][k];
      data[i][k] = data[j][k];
      data[j][k] = temp_data;
     }
      temp_teacher = teacher[i];
      teacher[i] = teacher[j];
      teacher[j] = temp_teacher;
  }
}
