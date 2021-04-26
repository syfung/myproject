# -*- coding: utf-8 -*-
"""
Created on Apr 25, 2021

@author: Joshua Fung
"""


class Song:
    def __init__(self, title, author, body, key=None, timesig=None):
        # Needs better data validation
        self.title = title.strip()
        self.author = author.strip()

        if key is not None:
            self.key = key.strip()
        else:
            self.key = key
        if timesig is not None:
            self.time = timesig.strip()
        else:
            self.time = timesig

        self.body = []
            
        # Main section
        section = Section('')
        self.sections = [section]

        for line in body.splitlines():
            line = line.strip()
            if line == '':
                continue
            i = line.find(':')
            
            # If line have ':', assume a setion or attribute
            # Always override if a tag exists
            if i > 0:
                tag = line[0:i]
                if tag.strip().lower() == 'title':
                    self.key = line[i+1:].strip()
                elif tag.strip().lower() == 'author':
                    self.key = line[i+1:].strip()
                elif tag.strip().lower() == 'key':
                    self.body.append(line)
                    self.key = line[i+1:].strip()
                elif tag.strip().lower() == 'time':
                    self.body.append(line)
                    self.time = line[i+1:].strip()
                else:
                     # New section, or else it is always in the default
                     section = Section(tag)
                     self.sections.append(section)
                     
            # Songlines
            #TODO fix minus one erro when the phrase end with a chord
            else:
                self.body.append(line)
                songline = Songline()
                j = 0
                k = 0
                while j < len(line):
                    if line[j] == '[':
                        j += 1
                        k = line[j:].find(']')
                        # Assume the cord always end properly 
                        songline.chords.append(line[j:k + j])
                        k += 1
                    else:
                        # Add empty chord
                        songline.chords.append('')
                        k = 0
                    j = j + k
                    if len(line) == j:
                        songline.phrases.append(' ')
                    else:
                        k = line[j:].find('[')
                        if k < 0:
                            k = len(line[j:])
                        songline.phrases.append(line[j:j+k])
                        j = j + k
                section.songlines.append(songline)
                # print(songline.chords, songline.phrases)
                
    def get_body_text(self):
        return '\n'.join([body for body in self.body])
        
    def __str__(self):   
        s = (self.title 
             + ' by ' 
             + self.author 
             + '\n'
             )
        if self.key is not None and self.key != '':
            s +=  ('Key: ' 
                   + self.key 
                   + '\n'
                   )
        if self.time is not None and self.time != '':
            s +=  ('Time: ' 
                   + self.time 
                   + '\n\n'
                   )
            s += '\n'.join([str(section) for section in self.sections])
        return s
    

class Section:
    def __init__(self, sectionName):
        self.sectionName = sectionName
        self.songlines = []
        
    def __str__(self):
        if self.songlines != []:
            return (self.sectionName 
                    + '\n' 
                    + ''.join([str(line) for line in self.songlines])
                    )
        else:
            return ''


class Songline:
    def __init__(self):
        self.chords = []
        self.phrases = []
        
    def getChordsPhrases(self):
        return zip(self.chords, self.phrases)
    
    def _print_array(self):
        print([self.chords, self.phrases])

    def __str__(self):
        chords_s = ''
        for phrase, chord in zip(self.phrases, self.chords):
            chords_s += chord.ljust(len(phrase))
        return (chords_s 
                + '\n' 
                + ''.join([str(phrase) for phrase in self.phrases]) 
                + '\n'
                )

if __name__ == "__main__":
    s = Song('test', 'test', 'Key: E\nTime: 4/4 \n讓[|] [Am](我)們回到那一[|] [D](秒)　你好不[|] [Bb](好)')
    print(s.get_body_text())
