#include <stdio.h>
#include <math.h>

#define MAX_DATA_NUMBER 100
#define MAX_ELEMENTS 50

// m行n列の行列の構造体
typedef struct{
  int m;
  int n;
  double data[MAX_ELEMENTS][MAX_ELEMENTS];
}matrix_r;

/*******************************************/
/* 関数PrintMatrix：行列の要素を表示する関数 */
/*******************************************/
void PrintMatrix(matrix_r mat){
  for ( int i = 0; i < mat.m; i++ ){
    for ( int j = 0; j < mat.n; j++ ){
      printf("%5.1f\t", mat.data[i][j]);
    }
    printf("\n");
  }
}
/********************************************/
/* 関数TransposeMatrix：転置行列を求める関数 */
/* 入力：行列src                            */
/* 出力：行列srcの転置行列dst                */
/********************************************/
void TransposeMatrix(matrix_r src, matrix_r *dst){
  // 関数の中身を記入してください
  for(int i = 0;i < src.m;i++){
    for(int j = 0;j < src.n;j++){
      dst->data[j][i] = src.data[i][j];
    }
  }
}

/*************************************************/
/* 関数MultiplyMatrix：2つの行列の積を計算する関数 */
/* 入力1：左から掛ける行列src1                    */
/* 入力2：右から掛ける行列src2                    */
/* 出力：行列src1と行列src2の積dst                */
/*************************************************/
int MultiplyMatrix(matrix_r src1, matrix_r src2, matrix_r *dst){
  // 関数の中身を記入してください
  // 掛け算ができない場合（要素数の不一致）、-1を返してください
  // 掛け算ができた場合は1を返してください
  int ans = 0;
  int aryM[src2.m];
  int aryN[src2.m];
  if (src1.n != src2.m){
    return -1;
  }else{
    for(int i=0 ; i < src1.m;i++ ){
      for(int j=0 ; j < src1.n;j++ ){
        for(int k=0 ; k < src2.m;k++ ){
          aryM[k] = src1.data[i][k];
          aryN[k] = src2.data[k][j];
        }
        for(int l=0; l < src1.n; l++){
          ans += aryM[l]*aryN[l];
        }
        dst->data[i][j] = ans;
      }
    }
    return 1;  
  }
}

/******************************************/
/* 関数InverseMatrix：逆行列を計算する関数 */
/* 入力：行列src                          */
/* 出力：行列srcの逆行列dst                */
/******************************************/
int InverseMatrix(matrix_r src, matrix_r *dst){
  // 関数の中身を記入してください
  // 逆行列が計算できない場合（正方行列でない）、-1を返してください
  // 逆行列が計算できた場合は1を返してください
  // 行列dstのサイズを設定する
  dst->m = src.m;
  dst->n = src.n;

  int sweepM = src.m;
  int sweepN = src.n;
  double a=0,b=0;
  for(int i=0 ;i<src.m ;i++ ){
    for(int j=0 ;j<src.n ;j++ ){
      if( i==j ){
        src.data[sweepM+i][sweepN+j] = 1; 
      }else{
        src.data[sweepM+i][sweepN+j] = 0;
      }
    }
  }
  if (src.m != src.n){
    return -1;
  }else{
    for(int i=0; i < src.m; i++){
      for(int j=0; j < src.m; j++){
        a = 1/src.data[i][j];
        src.data[i][j] *= a;
        b = -src.data[i][j];
        src.data[i][j] += b*src.data[i][j];
      }
    }
    for(int i=0; i < src.m; i++){
      for(int j=0; j < src.m; j++){
        dst->data[i][j] = src.data[sweepM+i][sweepN+j];
      }
    }
    return 1;
  }
}

int main (void){
  FILE *fp;
  double data[MAX_DATA_NUMBER][2];
  matrix_r mat_a, mat_at, mat_b;
  matrix_r mat_ata, invmat_ata, mat_atb;
  matrix_r mat_result;
  int data_number;

  // エラー防止のため
  mat_result.m = 3;
  mat_result.n = 1;

  // ファイルからデータを読み込む
  fp = fopen("data.txt", "r");
  fscanf(fp, "%d", &data_number);
  for ( int i = 0; i < data_number; i++ ){
    for ( int j = 0; j < 2; j++ ){
      fscanf(fp, "%lf", &data[i][j]);
    }
  }
  fclose(fp);

  //  行列Aに各要素の値を入れる
  mat_a.m = data_number;
  mat_a.n = 3;
  for ( int i = 0; i < data_number; i++ ){
    mat_a.data[i][0] = (double)(data[i][0] * data[i][0]);
    mat_a.data[i][1] = (double)data[i][0];
    mat_a.data[i][2] = 1.0;
  }

  // ベクトルbに各要素の値を入れる
  mat_b.m = data_number;
  mat_b.n = 1;
  for ( int i = 0; i < data_number; i++ ){
    mat_b.data[i][0] = (double)data[i][1];
  }

  // 行列mat_aの転置行列をmat_atとする
  TransposeMatrix(mat_a, &mat_at);
  // 行列mat_atと行列mat_aを掛けたものを行列mat_ataとする
  if ( MultiplyMatrix(mat_at, mat_a, &mat_ata) == -1 ){
    return 0;
  }
  // 行列mat_ataの逆行列を行列invmat_ataとする
  if ( InverseMatrix(mat_ata, &invmat_ata) == -1 ){
    return 0;
  }
  // 行列mat_atと行列mat_bを掛けたものを行列mat_atbとする
  if ( MultiplyMatrix(mat_at, mat_b, &mat_atb) == -1 ){
    return 0;
  }
  // 行列invmat_ataと行列mat_atbを掛けたものを行列mat_resultとする
  if ( MultiplyMatrix(invmat_ata, mat_atb, &mat_result) == -1 ){
    return 0;
  }

  // 求まった回帰式の表示
  printf("The regression equation is\n");
  printf("y = %2.1f x^2 ", mat_result.data[0][0]);
  if ( mat_result.data[1][0] > 0.0 ){
    printf("+ %2.1f x ", mat_result.data[1][0]);
  }
  else{
    printf("- %2.1f x ", -mat_result.data[1][0]);
  }
  if ( mat_result.data[2][0] > 0.0 ){
    printf("+ %2.1f\n", mat_result.data[2][0]);
  }
  else{
    printf("- %2.1f\n", -mat_result.data[2][0]);
  }	 

  return 0;
}
