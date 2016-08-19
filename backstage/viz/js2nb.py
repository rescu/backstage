"""
Some basic functions for injecting Javascript into Jupyter notebooks
"""

import os

import jinja2
import json
from IPython.display import HTML

def inject_d3js(d3js_filename, style=None, d3js_template_options={}, local_d3_install=None, return_string=False):
    """
    Take in the filename of the D3.js script, assumed to be a Jinja2 template,
    and generate the necessary HTML, plus styling if selected, to display in a
    notebook.
    """
    
    #configure environment
    env = jinja2.Environment(loader=jinja2.FileSystemLoader([os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates/'), os.path.dirname(d3js_filename)]))
    
    #grab style from stylesheet if it exists
    if style is None:
        style = ''
    else:
        with open(style,'r') as f:
            style = ''.join(f.readlines())
            
    #check if we've got a local install of d3.js 
    if local_d3_install is not None:
        path_to_d3 = local_d3_install
    else:
        path_to_d3 = 'https://cdnjs.cloudflare.com/ajax/libs/d3/4.2.2/d3.min.js'
    
    #grab the templates
    gen_template = env.get_template('inject_d3js.html')
    d3js_template = env.get_template(os.path.basename(d3js_filename))
    
    #render the d3js file
    d3js_text = d3js_template.render(object_id='d3DummyId',**d3js_template_options)
    
    #render the general template
    gen_text = gen_template.render(object_id='d3DummyId', style_sheet=style, path_to_d3=path_to_d3, d3js_text=d3js_text)
    
    if return_string:
        return gen_text
    else:
        return HTML(gen_text)
    