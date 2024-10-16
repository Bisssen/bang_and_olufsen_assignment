from api_interactor.text_gui import text_gui


json_object_to_string_pairs2 = [([{'id':1}], "{'id': 1}"),
                                ([{'name': 'bob'}], "{'name': 'bob'}"),
                                ([{'name': 'bob'}, {'id': 1}], "{'name': 'bob'}\n{'id': 1}"),
                                ([{'id': 1}, {'name': 'bob'}], "{'id': 1}\n{'name': 'bob'}"),
                                ([], '')]

mock_json_objects = [([{'id':1}]),
                     ([{'name': 'bob'}]),
                     ([{'name': 'bob'}, {'id': 1}]),
                     ([{'id': 1}, {'name': 'bob'}]),
                     ([])]

string_outputs = [("{'id': 1}"),
                    ("{'name': 'bob'}"),
                    ("{'name': 'bob'}\n{'id': 1}"),
                    ("{'id': 1}\n{'name': 'bob'}"),
                    ('')]

print(len(mock_json_objects[0]))
json_object_to_string_pairs = [tuple([tup]+[value]) for tup, value in zip(mock_json_objects, string_outputs)]
print(len(json_object_to_string_pairs[0]))
json_object_to_string_pairs = [list(tup)+[value] for tup, value in zip(json_object_to_string_pairs, string_outputs)]
print(len(json_object_to_string_pairs[0]))


print(mock_json_objects[0])
print(json_object_to_string_pairs[0])
print(json_object_to_string_pairs2[0])

import sys
sys.exit()

if __name__ == "__main__":
    from api_interactor.fetcher  import fetcher
    tmp = fetcher()
    print(tmp.convert_list_of_dicts_to_string( []) )
    gui: text_gui = text_gui()
    gui.loop()
