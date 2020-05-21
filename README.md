# NER_BiLSTM_IDCNN_CRF

+ 通用卷积神经网络在池化层存在信息丢失的现象，为了解决问题，学者提出了膨胀卷积神经网络。
+ 膨胀卷积神经网络（Dilated CNN)
  + 膨胀卷积的好处是不做pooling损失信息的情况下，加大了感受野，让每个卷积输出都包含较大范围的信息。在图像需要全局信息或者自然语言处理中需要较长是sequence信息依赖的问题中，都能很好的应用。膨胀卷积的filters本身没有变化。
  + 在tensorflow中的代码实现：
    + tf.nn.conv2d(value,filters,rate,padding,name=None)
    + value:输入的卷积图像，[batch,height,width,channels].
    + filters:卷积核,[filter_height,filter_width,channels,out_channels],通常NLP领域height设为1.
    + rate:正常的卷积通常会有stride，即卷集核滑动步长，而膨胀卷积核当中穿插的rate-1个0的个数，实现对原始数据采用间隔变大。
    + padding:"SAME":补零；“VALID”：丢弃多余的。
+ 迭代的膨胀卷积网络（IDCNN）
  + 模型是4个大相同结构的Dilated CNN block 拼在一起，每个block里面是dilation width为1，1，2的三层Dilated卷积层，所以叫做Iterated Dilated CNN。就是对膨胀卷积层进行了遍历。
  + ![image-20200521185215862](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20200521185215862.png)
+ 对文本使用卷集的维度表示：
  + 对文本做卷集时候，可以把文本看成高度为1的图片。图像的输入一般为4维，而文本的输入为3维度，所以首先要对文本输入维度进行扩维，一般在第一个维度进行。model_inputs = tf.expand_dims(model_inputs, 1)。
  + 文本的输入（batch_size,length,embedding),扩展后维度为（batch_size,1，length,embedding)。图像的输入为[batch_size,height,width,channels]。文本中embedding相当于图片中的通道，一张图片用3个通道表示，文本中的一个字用embedding维度表示。图片中卷集核是3*3的，文本的高度为1，所以文本卷集合为1*3的卷集核心。