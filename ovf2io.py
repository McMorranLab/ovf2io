from pathlib import Path
import shlex
import warnings

def create_header_entry(key, value, header):
    if key == "desc":
        # Start with empty list unless header already has {"desc": ["desc line 1"]}
        desc = header.get(key, [])
        desc += [value]
        return {"desc": desc}
    return {key: value}

def check_header_keys(header):
    mandatory_keys = {"title", "meshunit", "valueunits", "valuedim", "valuelabels", 
                     "xmin", "xmax", "ymin", "ymax", "zmin", "zmax",
                     "meshtype"}
    mandatory_rectangular_keys = {"xbase", "ybase", "zbase", 
                                  "xstepsize", "ystepsize", "zstepsize",
                                  "xnodes", "ynodes", "znodes"}
    mandatory_irregular_keys = {"pointcount"}
    missing_keys = mandatory_keys - set(header.keys())
    # Checking for missing keys
    if missing_keys != set():
        for key in missing_keys:
            raise Exception("Key '{}' is required, but was not found in the header. ".format(key))
    if header['meshtype'] == "rectangular":
        missing_rectangular_keys = mandatory_rectangular_keys - set(header.keys())
        for key in missing_rectangular_keys:
            raise Exception(f"Key '{key}' is required when meshtype is rectangular, "
                            "but was not found in the header. ")
    elif header['meshtype'] == 'irregular':
        missing_irregular_keys = mandatory_irregular_keys - set(header.keys())
        for key in missing_irregular_keys:
            raise Exception(f"Key '{key}' is required when meshtype is irregular, "
                            "but was not found in the header. ")
    # Checking for extra keys
    extra_keys = (set(header.keys()) - mandatory_keys 
                - mandatory_irregular_keys - mandatory_rectangular_keys - {'desc'})
    if extra_keys != set():
        for key in extra_keys:
            warnings.warn(f"'{key}' is not a recognized key. ")
    return

def format_header(header):
    floatkeys = {'xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax',
                 'xbase', 'ybase', 'zbase', 'xstepsize', 'ystepsize', 'zstepsize'}
    intkeys = {'valuedim', 'pointcount', 'xnodes', 'ynodes', 'znodes'}
    # transform floats to floats and ints to ints
    for key in floatkeys.intersection(set(header.keys())):
        header[key] = float(header[key])
    for key in intkeys.intersection(set(header.keys())):
        header[key] = int(header[key])
    # Split shell style - valuelabels uses "" for multi-word labels
    header['valueunits'] = shlex.split(header['valueunits'])
    header['valuelabels'] = shlex.split(header['valuelabels'])
    # Value units can be one (for all dimensions) or one for each dimension
    if len(header['valueunits']) < header['valuedim']:
        header['valueunits'] = [header['valueunits'][0] for i in range(header['valuedim'])]
    return header


def parse_header(f):
    header = {}
    for line in list(f):
        # '##' denotes the start of comments in each line
        line = line.decode("utf-8").partition("##")[0]
        # Return once end of header is found
        if line.lower().startswith("# end: header"):
            check_header_keys(header)
            header = format_header(header)
            print(header)
            return header
        # Each line is a "key : value" pair
        # Partition gives ["before sep", "", ""] if the separator (":" in this case) is not found
        keyvaluepair = line[1:].partition(":")
        if len(keyvaluepair[2]) > 0:
            # key is case-insensitive and spaces are ignored
            key = keyvaluepair[0].strip().lower()
            value = keyvaluepair[2].strip()
            header.update(create_header_entry(key, value, header))
    raise Exception("End of header not found. ")

def read_ovf(fname):
    fname = Path(fname)
    with open(fname, "rb") as f:
        if not b"2.0" in next(f):
            raise ValueError("This file does not appear to be OVF 2.0. "
                             "ovf2io does not support older OVF formats. ")
        while b"# begin: header" not in next(f).lower():
            pass
        header = parse_header(f)
        # print(header)

if __name__ == "__main__":
    read_ovf("nist_sample_ovfv2.ovf")
