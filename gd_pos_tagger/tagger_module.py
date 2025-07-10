import spacy
from spacy.tokens import Token
import torch
import torch.nn as nn
import pickle
import numpy as np
from spacy.language import Language
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


# Load vocabs
with open("vocab.pkl", "rb") as f:
    word_to_idx = pickle.load(f)

with open("tag_map.pkl", "rb") as f:
    idx_to_tag = pickle.load(f)

# Load embedding matrix
embedding_matrix = np.load("embedding_matrix.npy")

class PosTagger(nn.Module):
    def __init__(self, vocab_size, tagset_size, embed_dim=300, hidden_dim=256, dropout=0.5):
        super().__init__()
        embedding_tensor = torch.tensor(embedding_matrix, dtype=torch.float32)
        self.embedding = nn.Embedding.from_pretrained(embedding_tensor, freeze=False, padding_idx=word_to_idx["<pad>"])
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(dropout) 
        self.fc = nn.Linear(hidden_dim * 2, tagset_size)
            
    def forward(self, token_ids, lengths):
        embedded = self.embedding(token_ids)
        packed = pack_padded_sequence(embedded, lengths.cpu(), batch_first=True, enforce_sorted=False)
        packed_output, _ = self.lstm(packed)
        lstm_output, _ = pad_packed_sequence(packed_output, batch_first=True)
        dropped_output = self.dropout(lstm_output) 
        tag_scores = self.fc(dropped_output)
        return tag_scores
    
model = PosTagger(vocab_size=len(word_to_idx), tagset_size=len(idx_to_tag))
model.load_state_dict(torch.load("best_tagging_model.pt", map_location='cpu'))
model.eval()

# Define spaCy pipeline component
class TaggerPipe:
    def __init__(self, model, word_to_idx, idx_to_tag):
        self.model = model
        self.word_to_idx = word_to_idx
        self.idx_to_tag = idx_to_tag

    def __call__(self, doc):
        tokens = [token.text.lower() for token in doc]
        ids = [self.word_to_idx.get(t, self.word_to_idx["<unk>"]) for t in tokens]
        lengths = torch.tensor([len(ids)])
        tensor = torch.tensor([ids])

        with torch.no_grad():
            outputs = self.model(tensor, lengths)
            predictions = outputs.argmax(dim=-1).squeeze(0).tolist()

        for token, pred_idx in zip(doc, predictions):
            token.tag_ = self.idx_to_tag[pred_idx]
        return doc
    
    
@Language.factory("pos_tagger_pipe")
def create_tagger_pipe(nlp, name):
    return TaggerPipe(model, word_to_idx, idx_to_tag)
