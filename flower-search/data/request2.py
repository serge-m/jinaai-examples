#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import numpy as np
# import matplotlib.pyplot as plt
# import base64


# In[2]:


from jina.flow import Flow
from pkg_resources import resource_filename
from PIL import Image
import os
import io

os.environ['PARALLEL'] = str(4)
os.environ['SHARDS'] = str(2)
os.environ['DATA_DIR'] = 'data/jpg'
os.environ['COLOR_CHANNEL_AXIS'] = str(0)
os.environ['JINA_PORT'] = str(45678)
os.environ['ENCODER'] = 'yaml/encode.yml'
os.environ['WORKDIR'] = 'data/workspace'
os.environ['TMP_WORKSPACE'] = 'data/workspace'
f = Flow.load_config('./flow-query.yml')


# In[3]:


f.use_grpc_gateway()


# In[4]:


result_html = []

def print_result(resp):
    for d in resp.search.docs:
        vi = d.uri
        result_html.append(f'<tr><td><img src="{vi}"/></td><td>')
        for match in d.matches:
            im = Image.open(io.BytesIO(match.meta_info))
            fname="{}.jpg".format(match.id)
            fname = os.path.join(os.environ['TMP_RESULTS'], fname)
            im.save(fname)
            result_html.append(f'<img src="{fname}" />')
        result_html.append('</td></tr>\n')


def write_html(html_path):
    with open(resource_filename('jina', '/'.join(('resources', 'helloworld.html'))), 'r') as fp,             \
            open(html_path, 'w') as fw:
        t = fp.read()
        t = t.replace('{% RESULT %}', '\n'.join(result_html))
        fw.write(t)

    # url_html_path = 'file://' + os.path.abspath(html_path)

    # try:
    #     webbrowser.open(url_html_path, new=2)
    # except:
    #     pass
    


# In[ ]:


image_src = './data/**/*.jpg'
with f:
    f.search_files(image_src, sampling_rate=.01, batch_size=8, output_fn=print_result, top_k=5)


# In[ ]:


write_html('./data/result.html')


# In[ ]:




