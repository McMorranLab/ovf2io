import math
import struct
import shlex
import warnings
import numpy as np
from . import _templates

def _create_header_entry(key, value, header):
    """Create a new header entry. 
    Basically just deals with 'desc' having multiple entries.
    """
    if key == "desc":
        # Start with empty list unless header already has {"desc": ["desc line 1"]}
        desc = header.get(key, [])
        desc += [value]
        return {"desc": desc}
    return {key: value}

def _check_header_keys(header):
    """Check for missing or extra header keys.

    Warns if extra, raises Exception if missing. 
    """
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

def _format_header(header):
    """Formats the header entries. 

    Deals with floats, ints, and lists. 
    """
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


def _parse_header(f):
    header = {}
    for line in f:
        # '##' denotes the start of comments in each line
        line = line.decode("utf-8").partition("##")[0]
        # Return once end of header is found
        if line.lower().startswith("# end: header"):
            _check_header_keys(header)
            header = _format_header(header)
            return header
        # Each line is a "key : value" pair
        # Partition gives ["before sep", "", ""] if the separator (":" in this case) is not found
        keyvaluepair = line[1:].partition(":")
        if len(keyvaluepair[2]) > 0:
            # key is case-insensitive and spaces are ignored
            key = keyvaluepair[0].strip().lower()
            value = keyvaluepair[2].strip()
            header.update(_create_header_entry(key, value, header))
    raise Exception("End of header not found. ")

def _advance_to_data_block(f):
    mode = ""
    nbytes = None
    for line in f:
        line = line.decode("utf-8")
        if "# begin: data" in line.lower():
            mode = line.split()[3]
            if mode.lower() == "binary":
                nbytes = int(line.split()[4])
                _check_first_byte(f, nbytes)
            return nbytes
    raise Exception("Beginning of data block not found. ")

def _parse_data(f, header, nbytes):
    if header['meshtype'] == 'rectangular':
        shape = (header['valuedim'], header['xnodes'], header['ynodes'], header['znodes'])
        keys = header['valuelabels']
    elif header['meshtype'] == 'irregular':
        shape = ((3 + header['valuedim'], header['pointcount']))
        keys = ["x", "y", "z"] + header['valuelabels']
    else:
        raise Exception("Meshtype not understood. ")
    count = math.prod(shape)
    sep = " " if nbytes is None else ""
    dtype = float if nbytes is None else f'<{"d" if nbytes == 8 else "f"}'
    array = np.fromfile(f, count=count, sep=sep, dtype=dtype).reshape(shape, order='F')
    out = {key: array[i] for i, key in enumerate(keys)}
    return out

def _gen_coords(data, header):
    if header['meshtype'] == 'rectangular':
        xcoords = header['xmin'] + header['xstepsize'] * (1/2 + np.arange(header['xnodes']))
        ycoords = header['ymin'] + header['ystepsize'] * (1/2 + np.arange(header['ynodes']))
        zcoords = header['zmin'] + header['zstepsize'] * (1/2 + np.arange(header['znodes']))
        x, y, z = np.meshgrid(xcoords, ycoords, zcoords, indexing='ij')
        return {'x': x, 'y': y, 'z': z}
    elif header['meshtype'] == 'irregular':
        # coords = np.einsum('i...->...i', np.array([data['x'], data['y'], data['z']]))
        x = data.pop("x")
        y = data.pop("y")
        z = data.pop("z")
        return {'x': x, 'y': y, 'z': z}

def _check_first_byte(f, nbytes):
    binrep = {4: ("<f", 1234567.0), 8: ("<d", 123456789012345.0)}
    test_value = struct.unpack(binrep[nbytes][0], f.read(nbytes))[0]
    if test_value != binrep[nbytes][1]:
        raise Exception("This binary file cannot be read. "
                        "The test value does not match. ")
    


##################################################
################### Write OVF #######################
##################################################

def _generate_coordinates(x, y, z, shape, meshtype):
    generated = False
    if x is None and y is None and z is None:
        x = np.arange(shape[0]) if meshtype == 'rectangular' else np.arange(shape[0])
        y = np.arange(shape[1]) if meshtype == 'rectangular' else np.zeros(shape[0])
        z = np.arange(shape[2]) if meshtype == 'rectangular' else np.zeros(shape[0])
        generated = True
    elif x is None or y is None or z is None:
        raise ValueError("x, y, and z must either all be given or all omitted. ")
    return x, y, z, generated

def _generate_valueunits_list(valueunits, valuedim):
    if len(valueunits) == 0:
        valueunits = ["1" for a in range(valuedim)]
    elif len(valueunits) == 1:
        valueunits = [valueunits[0] for a in range(valuedim)]
    elif len(valueunits) != valuedim:
        raise ValueError("Length of valueunits must be 1 or match"
                         " the number of data dimensions. ")
    return shlex.join(valueunits)

def _generate_valuelabels_list(valuelabels, valuedim):
    if len(valuelabels) == 0:
        valuelabels = [f"value_{n}" for n in range(valuedim)]
    elif len(valuelabels) != valuedim:
        raise ValueError("Length of valuelabels must match "
                         "the number of data dimensions. ")
    return shlex.join(valuelabels)

def _shape_desc(desc):
    s = "# desc: OVF file generated by ovf2io.py."
    for line in desc:
        s += "\n# desc: " + line
    return s

def _make_header(header, representation):
    rep = {"text": "text", "bin4": "Binary 4", "bin8": "Binary 8"}[representation]
    if header['meshtype'] == 'rectangular':
        frontmatter = _templates.rectangular_template
    else:
        frontmatter = _templates.irregular_template
    for key in header.keys():
        frontmatter = frontmatter.replace(f"[{key}]", str(header[key]))
    frontmatter = frontmatter.replace("[repr]", rep)
    return frontmatter

def _format_data(data, meshtype, x, y, z):
    if meshtype == "rectangular":
        reshaped = data.reshape((-1, data.shape[-1]), order='F')
    else:
        reshaped = np.zeros((data.shape[0], data.shape[1] + 3))
        reshaped[:, 0] = x
        reshaped[:, 1] = y
        reshaped[:, 2] = z
        reshaped[:, 3:] = data
    return reshaped

def _write_file(fname, frontmatter, representation, reshaped):
    with open(fname, "wb") as f:
        f.write(frontmatter.encode("utf-8"))
        binrep = {"bin4": ("<f", 1234567.0), "bin8": ("<d", 123456789012345.0)}
        if representation in binrep:
            f.write(struct.pack(*binrep[representation]))
            f.write(reshaped.astype(binrep[representation][0]).tobytes())
            f.write("\n".encode("utf-8"))
        else:
            np.savetxt(f, reshaped)
        rep = {"text": "text", "bin4": "Binary 4", "bin8": "Binary 8"}[representation]
        f.write(f"# End: Data {rep}".encode("utf-8"))
        f.write("\n# End: Segment".encode("utf-8"))

