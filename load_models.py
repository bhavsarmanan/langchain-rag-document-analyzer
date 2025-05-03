import subprocess

def load_models():


    model_list = subprocess.run(['ollama', 'list'], 
                                capture_output=True, 
                                text=True)
        
    lines = model_list.stdout.strip().split('\n')

    models = []
    for line in lines[1:]:  # Skip the header line
        if line.strip():  # Check if line is not empty
            model_name = line.split()[0]
            if  model_name.split(':')[0] != 'qwen3' and model_name.split(':')[0] != 'snowflake-arctic-embed2' and model_name.split(':')[0] != 'mxbai-embed-large': # First column is model name
                models.append(model_name.split(':')[0])
            if model_name.split(':')[0] == 'qwen3':
                models.append(model_name)



    return models