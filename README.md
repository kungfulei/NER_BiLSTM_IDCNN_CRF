# NER_BiLSTM_IDCNN_CRF

## 数据集标注方式

+ BIO标注集
  + B-PER、I-PER代表人名首字、人名非首字;
  + B-LOC、I-LOC代表地名首字、地名非首字;
  + B-ORG、I-ORG代表组织机构名首字、 组织机构名非首字; 
  + 0代表该字不属于命名实体的一部分。
+ BIOSE标注集
  + B-PER、 I-PER、 E-PER代表人名首字、人名中间字、人民末尾字;
  + B-LOC、 I-LOC、 E-PER代表地名首字、地名中间字、地名末尾字;
  + B-ORG、I-ORG、 E-PER代表组织机构名首字、组织机构名中间字、组织机构名末尾字;
  + S-X代表单字构成的实体;
  + 0代表该字不属于命名实体的一部分。



## BiLstm+ CRF

+ 模型架构
<<<<<<< HEAD
  
=======
  + ![1590067197(1)](https://github.com/kungfulei/NER_BiLSTM_IDCNN_CRF/blob/master/image/1590067343(1).png)
  + 


## IDCNN+CRF

+ 通用卷积神经网络在池化层存在信息丢失的现象，为了解决问题，学者提出了膨胀卷积神经网络。

+ 膨胀卷积神经网络（Dilated CNN)
  + 膨胀卷积的好处是不做pooling损失信息的情况下，加大了感受野，让每个卷积输出都包含较大范围的信息。在图像需要全局信息或者自然语言处理中需要较长是sequence信息依赖的问题中，都能很好的应用。膨胀卷积的filters本身没有变化。
  
  + 在tensorflow中的代码实现：
    ```python
    tf.nn.atrous_conv2d(value,filters,rate,padding,name=None）
    ```
    
    + value: 指需要做卷积的输入图像，要求是一个4维Tensor，具有`[batch, height, width, channels]`这样的shape，具体含义是[训练时一个batch的图片数量, 图片高度, 图片宽度, 图像通道数] .
    + filters:相当于CNN中的卷积核，要求是一个4维Tensor，具有[filter_height, filter_width, channels, out_channels]这样的shape，具体含义是[卷积核的高度，卷积核的宽度，图像通道数，卷积核个数]，同理这里第三维channels，就是参数value的第四维,通常NLP领域height设为1.
    + rate:正常的卷积通常会有stride，即卷集核滑动步长，而膨胀卷积核当中穿插的rate-1个0的个数，实现对原始数据采用间隔变大。
    + padding:"SAME":补零；“VALID”：丢弃多余的。
  
+ 迭代的膨胀卷积网络（IDCNN）
  
  + IDCNN就是对膨胀卷积层进行了遍历。模型是4个大相同结构的Dilated CNN block 拼在一起，每个block里面是dilation width为1，1，2的三层Dilated卷积层，所以叫做Iterated Dilated CNN。
  
  
  
+ 模型架构
  
  + ![1590067123(1)](https://github.com/kungfulei/NER_BiLSTM_IDCNN_CRF/blob/master/image/1590070582(1).png)
  
+ 对文本使用卷集的维度表示：
  + 对文本做卷集时候，可以把文本看成高度为1的图片。图像的输入一般为4维，而文本的输入为3维度，所以首先要对文本输入维度进行扩维，一般在第一个维度进行。model_inputs = tf.expand_dims(model_inputs, 1)。
  + 文本的输入（batch_size,length,embedding),扩展后维度为（batch_size,1，length,embedding)。图像的输入为[batch_size,height,width,channels]。文本中embedding相当于图片中的通道，一张图片用3个通道表示，文本中的一个字用embedding维度表示。图片中卷集核是3 * 3的，文本的高度为1，所以文本卷集合为1 * 3的卷集核心。
  
  
