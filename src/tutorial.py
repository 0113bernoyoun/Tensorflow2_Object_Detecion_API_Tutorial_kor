import torch.nn as nn

import torch.nn.functional as F

class ListenAttendSpell(nn.Module):

       """

       Listen, Attend and Spell (LAS) Model

​

       Args:

              - listener (nn.Module): encoder of seq2seq

              - speller (nn.Module): decoder of seq2seq

              - decode_function (nn.functional): A function used to generate symbols from RNN hidden state

​

       Reference:

              「Listen, Attend and Spell」 paper

              https://arxiv.org/abs/1508.01211

​

       How to Use:

              >>> listener = Listener(feat_size, 256, 0.5, 6, True, 'gru', True)

              >>> speller = Speller(vocab_size, 120, 8, 256 << (1 if use_bidirectional else 0))

              >>> model = ListenAttendSpell(listener, speller)

       """

       def __init__(self, listener, speller, decode_function = F.log_softmax, use_pyramidal = False):

              super(ListenAttendSpell, self).__init__()

              self.listener = listener

              self.speller = speller

              self.decode_function = decode_function

              self.use_pyramidal = use_pyramidal


       def forward(self, feats, targets=None, teacher_forcing_ratio=0.90, use_beam_search = False):

              listener_outputs, listener_hidden = self.listener(feats)

              y_hat, logit = self.speller(

                     inputs=targets,

                     listener_hidden=listener_hidden,

                     listener_outputs=listener_outputs,

                     function=self.decode_function,

                     teacher_forcing_ratio=teacher_forcing_ratio,

                     use_beam_search=use_beam_search

              )

              return y_hat, logit