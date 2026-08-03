from pathlib import Path
import yaml


def test_all_architecture_diagrams_use_section_10_1_reference_size():
    diagrams=[]
    for path in sorted(Path('state/content').glob('*.yaml')):
        data=yaml.safe_load(path.read_text(encoding='utf-8')) or {}
        for block in data.get('blocks', []):
            if block.get('type') == 'diagram':
                diagrams.append((path.name, block.get('title'), block.get('size')))
    assert diagrams
    assert all(size == 'standard' for _, _, size in diagrams), diagrams
