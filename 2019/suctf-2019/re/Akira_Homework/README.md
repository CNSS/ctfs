# Akira Homework

首先随便调一调，把反调试都给 patch 掉，大概有一些在 tls 里还有一些散布在执行过程中，有几个 timeout 也 patch 掉方便调试，这些 anti 全都可以通过给 exit、 TerminateProcess 等下断点然后回溯来 patch 掉。程序读 signature 的时候是个非法文件名，读进来 64Bytes 取个 md5，实际上是按 strlen 来算的长度，尝试 chamd5 一下结果得到了 signature，之后的验证放在一个 dll 中，线程也是新建的，稍微跟踪一下改一改跳一跳就能看到 flag。

input: Akira_aut0_ch3ss_!
sigature: Overwatch
sign: Ak1i3aS3cre7K3y

