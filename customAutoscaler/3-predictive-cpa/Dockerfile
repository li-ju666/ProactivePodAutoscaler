FROM custompodautoscaler/python:latest
RUN apt-get update
RUN apt-get install jq curl vim python3-pip wget gettext -y
RUN pip3 install keras tensorflow sklearn joblib pandas
RUN pip3 install statsmodels
ADD config.tmp evaluate.py metric.py updateModel.py start.sh __init__.py helpers.py /
RUN mkdir -p /model_dir
# ADD model_files /model_files/
# Set up aliases for easy debugging
RUN echo 'alias metrics="curl -X GET http://localhost:5000/api/v1/metrics | jq ."' >> ~/.bashrc
RUN echo 'alias evaluation="curl -X POST http://localhost:5000/api/v1/evaluation | jq ."' >> ~/.bashrc
CMD /start.sh
