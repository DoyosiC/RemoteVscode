#include <stdio.h>
#include <math.h>

#define MAX_ELEMENTS 100
#define INPUT_UNITS 5
#define OUTPUT_UNITS 3

// 各層のユニットの値
typedef struct {
    int n;  // ユニット数
    double unit[MAX_ELEMENTS]; // 各ユニットの値
} layer_r;

// 第1層から第2層への重み行列
typedef struct {
    int m;  // 第1層のユニット数
    int n;  // 第2層のユニット数
    double data[MAX_ELEMENTS][MAX_ELEMENTS];  // 重み行列
} weight_r;

/******************************************************/
/* 関数PrintLayer：層のユニットの値を表示する関数 */
/******************************************************/
void PrintLayer(layer_r layer) {
    for (int i = 0; i < layer.n; i++) {
        printf("%3.3f\t", layer.unit[i]);
    }
    printf("\n");
}

/*********************************************************************/
/* 関数MultiplyMatrix：重み行列と入力ベクトルの積を計算する関数 */
/* 入力1：重み行列src1                                     */
/* 入力2：入力ベクトルsrc2                                 */
/* 出力：出力ベクトルdst                                   */
/*********************************************************************/
int MultiplyMatrix(weight_r src1, layer_r src2, layer_r *dst) {
    if (src1.m != src2.n) {
        printf("Multiply Matrix Error\n");
        return -1;
    }
    dst->n = src1.n;
    for (int i = 0; i < src1.n; i++) {
        dst->unit[i] = 0;
        for (int j = 0; j < src2.n; j++) {
            for (int k = 0; k < src1.m; k++) {
                dst->unit[i] += src1.data[i][k] * src2.unit[k];
            }
        }
    }
    return 1;
}

/***************************************************/
/* 関数Sigmoid：sigmoid関数を層に適用する関数  */
/* 関数Softmax：softmax関数を層に適用する関数  */
/* 関数Relu：ReLu関数を層に適用する関数         */
/* 入力：input    出力：output              */
/***************************************************/

/****************************************************/
/* 以上の３つの活性化関数の中身を記述してください */
/****************************************************/
void Sigmoid(layer_r input, layer_r *output) {
    output->n = input.n; 

    for (int i = 0; i < input.n; i++) {
        output->unit[i] = 1 / (1 + exp(-input.unit[i]));
    }
}

void Softmax(layer_r input, layer_r *output) {
    output->n = input.n; 

    double sum = 0.0;
    for (int i = 0; i < input.n; i++) {
        output->unit[i] = exp(input.unit[i]);
        sum += output->unit[i];
    }
    for (int i = 0; i < input.n; i++) {
        output->unit[i] /= sum;
    }
}

void Relu(layer_r input, layer_r *output) {
    output->n = input.n; 

    for (int i = 0; i < input.n; i++) {
        output->unit[i] = (input.unit[i] > 0) ? input.unit[i] : 0;
    }
}

int main(void) {
    layer_r input_l, output_l;
    weight_r weights;
    layer_r sig_l, soft_l, relu_l;

    // 入力層に値を入力（ユニット数はINPUT_UNITS=5）
    // 値は0.0, 0.1, 0.2, 0.3, 0.4とする
    input_l.n = INPUT_UNITS;
    for (int i = 0; i < input_l.n; i++) {
        input_l.unit[i] = (double)i * 0.1;
    }

    // 出力層のユニット数（OUTPUT_UNITS=3）を入力
    output_l.n = OUTPUT_UNITS;

    // 重みベクトルに値を入力
    weights.m = input_l.n;
    weights.n = output_l.n;
    for (int j = 0; j < weights.n; j++) {
        for (int i = 0; i < weights.m; i++) {
            weights.data[j][i] = (double)(i + 1) * 0.1 + (double)(j + 1) * 0.1;
        }
    }

    // 出力ベクトルの値を計算する（活性化関数前）
    MultiplyMatrix(weights, input_l, &output_l);

    // 出力層に各活性化関数を適用する
    Sigmoid(output_l, &sig_l);
    Softmax(output_l, &soft_l);
    Relu(output_l, &relu_l);

    // 活性化関数前の出力層のユニット値と適用後のユニット値を表示する
    printf("活性化関数適用前の出力層\n");
    PrintLayer(output_l);
    printf("\nsigmoid関数適用後の出力層\n");
    PrintLayer(sig_l);
    printf("\nsoftmax関数適用後の出力層\n");
    PrintLayer(soft_l);
    printf("\nReLu関数適用後の出力層\n");
    PrintLayer(relu_l);

    return 0;
}
