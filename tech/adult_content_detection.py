from nsfw_detector import predict
import streamlit as st

model = predict.load_model('nsfw_mobilenet.h5')

# Predict single image
result = predict.classify(model, 'sex.jpeg')
st.write(result)
# {'2.jpg': {'sexy': 4.3454722e-05, 'neutral': 0.00026579265, 'porn': 0.0007733492, 'hentai': 0.14751932, 'drawings': 0.85139805}}
