# -*- coding: utf-8 -*-
import pytest

from mychordsheets.song import *

@pytest.mark.parametrize(('title', 'author', 'body', 'key', 'timesig', 'chords', 'lyrics', 'section', 'line'), (
    ('Test Title', 'Test Author', '[E]L[E]L', 'A', '4/4', ['E', 'E'], ['L', 'L'], 0, 0),
    ('Test Title', 'Test Author', '[E ]L', 'A', '4/4', ['E '], ['L'], 0, 0),
    ('Test Title', 'Test Author', '[E]L ', 'A', '4/4', ['E'], ['L'], 0, 0),
    ('Test Title', 'Test Author', 'L [E] ', 'A', '4/4', ['', 'E'], ['L ', ' '], 0, 0),
    ('Test Title', 'Test Author', ' [E]', 'A', '4/4', ['E'], [' '], 0, 0),    
    ('Test Title', 'Test Author', ' [E]', 'A', '4/4', ['E'], [' '], 0, 0),    
    ('Test Title', 'Test Author', 'V1:\n [E]', 'A', '4/4', ['E'], [' '], 1, 0),
    ('Test Title', 'Test Author', 'V1:\n [E]\n [E]', 'A', '4/4', ['E'], [' '], 1, 1),
    ('Test Title', 'Test Author', 'Key:A\nTime:4/4\nV1:\n\n\n [E]\n [E]', 'A', '4/4', ['E'], [' '], 1, 1),
    ('Test Title', 'Test Author', 'V1:\n\n\n [E]\n [E]', None, None, ['E'], [' '], 1, 1),
))

def test_song(title, author, body, key, timesig, chords, lyrics, section, line):
    s = Song(title, author, body, key, timesig)
    assert s.title in title
    assert title in str(s)
    assert s.author in author 
    assert s.key == key
    assert s.time == timesig
    assert s.sections[section].songlines[line].chords == chords
    assert s.sections[section].songlines[line].phrases == lyrics
    assert isinstance(s.sections[section].songlines[line].getChordsPhrases(), zip)
    s.sections[section].songlines[line]._print_array()
    print(repr(s.sections[section]),repr(s), repr(s.sections[section].songlines[line]))

@pytest.mark.parametrize(('title', 'author', 'body', 'out_s'), (
    ('Test',
     'Test',
     'Key:A\nTime:4/4\n[E]L[E]L\nV1:\n\n\n [E]\n [E]',
     'Key: A\nTime: 4/4\n\n\nEE\nLL\n\nV1\nE\n \nE\n \n'),
    ('My Song ',
     ' Author ',
     'Key: E\nTime: 4/4 \n讓[|] [Am](我)們回到那一[|] [D](秒)　你好不[|] [Bb](好)',
     'Key: E\nTime: 4/4\n\n\n |Am      |D      |Bb \n讓 (我)們回到那一 (秒)　你好不 (好)\n'),
))

def test_song_string(title, author, body, out_s):
    s = Song(title, author, body)
    print(s)
    assert str(s) == (title.strip() + ' by ' + author.strip() + '\n' + out_s)
