import os
import sys
import utils.util as util
import model.model as cluster
import utils.extract_text as extract_text

# if you want to change the model, re-run the line below with the appropriate model k_means;c_means
# model = cluster.ClusterModel(model='k_means')

def main():
    in_path = 'input/'
    out_path = 'output/'

    files = [file for file in os.listdir(in_path)
            if file.endswith('.pdf')]

    for file in files:
        print(f'\r File {file} is in process ...', end= '')
        sys.stdout.flush()
        cluster = util.prediction(os.path.join(in_path,file)) 

        os.makedirs(os.path.join(out_path,str(cluster[0])), exist_ok=True)
        os.rename(os.path.join(in_path,file), os.path.join(out_path,str(cluster[0]),file))
        
    print(f'\r Process is done.', end= '')

def restore():
    in_path = 'input/'

    for parent, _, filenames in os.walk('output/'):
        for fn in filenames:
            if fn.lower().endswith('.pdf'):
                os.rename(os.path.join(parent, fn), os.path.join(in_path, fn))
                
if __name__ == "__main__":
    main()
    restore()