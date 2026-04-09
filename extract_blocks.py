import codecs
import os

def extract():
    with codecs.open('simulasyon_11.py', 'r', 'utf-8') as f:
        content = f.readlines()
    
    if not os.path.exists('scratch'):
        os.makedirs('scratch')
        
    def save(name, lines):
        with codecs.open(os.path.join('scratch', name), 'w', 'utf-8') as f:
            f.writelines(lines)
            
    # adjusted indices (lines are 1-based in view_file, 0-based in list)
    save('block1.txt', content[5764:6005])
    save('block2.txt', content[6016:6546])
    save('block3.txt', content[6556:6832])
    save('main1.txt', content[6007:6010])
    save('main2.txt', content[6546:6551])
    save('dup_phase3.txt', content[555:619])

if __name__ == "__main__":
    extract()
