import struct
from enum import Enum


class DressupCategory(Enum):
    Base = 0
    Accessory = 1
    Bag = 2 
    Eye = 3
    Foot = 4
    Glove = 5
    Head = 6
    Hair = 7
    Leg = 8 
    Dress = 9
    Face = 10
    LowerBody = 11
    UpperBody = 12
    Max = 13


class StyleCategory(Enum):
    SkinColor = 0
    LipColor = 1
    DarkCircleColor = 2 
    EyeColor = 3
    EyebrowsColor = 4
    EyebrowsVolume = 5
    EyelashesColor = 6
    EyelashesVolume = 7
    Mole = 8
    Mole_01 = 9
    Freckles = 10
    HairColor_00 = 11
    HairColor_01 = 12
    HairColor_02 = 13
    HairColor_03 = 14
    ShapeFace = 15
    ShapeFhr = 16
    HairColorStyle = 17
    Max = 18


# Category name mappings
DRESSUP_CATEGORY_NAMES = [
    "base", "acc", "bag", "eyw", "ftw", "glv", "hdw", "hrs",
    "lgw", "drs", "face", "lwb", "upb"
]

STYLE_CATEGORY_NAMES = [
    "color_skin", "color_lip", "color_darkcircle", "color_eye",
    "color_eyebrow", "volume_eyebrow", "color_eyelash", "volume_eyelash",
    "mole", "mole_01", "freckles", "color_hrs_00", "color_hrs_01",
    "color_hrs_02", "color_hrs_03", "shape_face", "shape_fhr", "style_hrs"
]


class SaveData:
    SIZE = 176

    def __init__(self):
        # Dressup labels (13 categories × 8 bytes = 104 bytes)
        self.dressup_labels = [0] * len(DressupCategory)

        # Style data (18 categories × 4 bytes = 72 bytes)
        self.style_data = [0] * len(StyleCategory)

    @classmethod
    def from_bytes(cls, data):
        """Parse SaveData from 176 bytes of data"""
        if len(data) != cls.SIZE:
            raise ValueError(f"SaveData requires {cls.SIZE} bytes, got {len(data)}")

        save_data = cls()

        # Parse dressup labels (13 uint64 values)
        for i in range(len(DressupCategory) - 1):
            start = i * 8
            end = start + 8
            save_data.dressup_labels[i] = struct.unpack('<Q', data[start:end])[0]

        # Parse style data (18 int32 values)
        style_start = 104 # After 13×8 = 104 bytes
        for i in range(len(StyleCategory) - 1):
            start = style_start + (i * 4)
            end = start + 4
            save_data.style_data[i] = struct.unpack('<i', data[start:end])[0]

        return save_data

    def to_bytes(self):
        """Convert SaveData back to bytes"""
        data = b''

        # Pack dressup labels
        for label in self.dressup_labels:
            data += struct.pack('<Q', label)

        # Pack style data
        for style in self.style_data:
            data += struct.pack('<i', style)

        return data

    def get_dressup_hash(self, category_index):
        """Get dressup hash for a category"""
        if 0 <= category_index < len(self.dressup_labels):
            return self.dressup_labels[category_index]
        return 0

    def set_dressup_hash(self, category_index, hash_value):
        """Set dressup hash for a category"""
        if 0 <= category_index < len(self.dressup_labels):
            self.dressup_labels[category_index] = hash_value

    def get_style_index(self, category_index):
        """Get style index for a category"""
        if 0 <= category_index < len(self.style_data):
            return self.style_data[category_index]
        return 0

    def set_style_index(self, category_index, style_index):
        """Set style index for a category"""
        if 0 <= category_index < len(self.style_data):
            self.style_data[category_index] = style_index

    def __str__(self):
        dressup_str = ", ".join(f"{DRESSUP_CATEGORY_NAMES[i]}:0x{label:016x}"
                                for i, label in enumerate(self.dressup_labels) if label != 0)
        style_str = ", ".join(f"{STYLE_CATEGORY_NAMES[i]}:{style}"
                              for i, style in enumerate(self.style_data) if i < len(StyleCategory) - 1)
        return f"SaveData(Dressup: [{dressup_str}], Styles: [{style_str}])"


class CopyDressUpSaveData:
    SIZE = 104

    def __init__(self):
        # Dressup labels only (13 categories × 8 bytes = 104 bytes)
        self.dressup_labels = [0] * len(DressupCategory)

    @classmethod
    def from_bytes(cls, data):
        """Parse CopyDressUpSaveData from 104 bytes of data"""
        if len(data) != cls.SIZE:
            raise ValueError(f"CopyDressUpSaveData requires {cls.SIZE} bytes, got {len(data)}")

        copy_data = cls()

        # Parse dressup labels (13 uint64 values)
        for i in range(len(DressupCategory)):
            start = i * 8
            end = start + 8
            copy_data.dressup_labels[i] = struct.unpack('<Q', data[start:end])[0]

        return copy_data

    def to_bytes(self):
        """Convert CopyDressUpSaveData back to bytes"""
        data = b''
        for label in self.dressup_labels:
            data += struct.pack('<Q', label)
        return data

    def get_dressup_hash(self, category_index):
        """Get dressup hash for a category"""
        if 0 <= category_index < len(self.dressup_labels):
            return self.dressup_labels[category_index]
        return 0

    def set_dressup_hash(self, category_index, hash_value):
        """Set dressup hash for a category"""
        if 0 <= category_index < len(self.dressup_labels):
            self.dressup_labels[category_index] = hash_value

    def is_empty(self):
        """Check if all dressup labels are zero (no stored data)"""
        return all(label == 0 for label in self.dressup_labels)

    def __str__(self):
        dressup_str = ", ".join(f"{DRESSUP_CATEGORY_NAMES[i]}:0x{label:016x}"
                                for i, label in enumerate(self.dressup_labels) if label != 0)
        return f"CopyDressUpSaveData([{dressup_str}])"


class PlayerSaveDataAccessor:
    def __init__(self):
        self.save_data = SaveData()
        self.copy_dressup_data = CopyDressUpSaveData()
        # Note: The C++ class also has Rotom save data, but it's not detailed in the header

    # Main data access methods
    def set_dressup_hash(self, category_index, hash_value):
        """Set dressup hash for a category"""
        self.save_data.set_dressup_hash(category_index, hash_value)

    def get_dressup_hash(self, category_index):
        """Get dressup hash for a category"""
        return self.save_data.get_dressup_hash(category_index)

    def set_style_index(self, category_index, style_index):
        """Set style index for a category"""
        self.save_data.set_style_index(category_index, style_index)

    def get_style_index(self, category_index):
        """Get style index for a category"""
        return self.save_data.get_style_index(category_index)

    # Copy dressup data methods (for random dressup feature)
    def set_store_current_dressup_info(self):
        """Store current dressup info to copy buffer"""
        # Copy all dressup labels from main data to copy data
        for i in range(len(DressupCategory)):
            self.copy_dressup_data.dressup_labels[i] = self.save_data.dressup_labels[i]

    def apply_stored_dressup_info(self):
        """Apply stored dressup info from copy buffer"""
        # Copy all dressup labels from copy data to main data
        for i in range(len(DressupCategory)):
            self.save_data.dressup_labels[i] = self.copy_dressup_data.dressup_labels[i]

    def is_stored_dressup_info(self):
        """Check if there's stored dressup info"""
        return not self.copy_dressup_data.is_empty()

    def clear_stored_dressup_info(self):
        """Clear stored dressup info"""
        self.copy_dressup_data = CopyDressUpSaveData()

    # File I/O methods
    @classmethod
    def from_bytes(cls, player_data, copy_dressup_data=None, rotom_data=None, style_data=None):
        """
        Create PlayerSaveDataAccessor from binary data

        Args:
            player_data: 176 bytes of SaveData
            copy_dressup_data: 104 bytes of CopyDressUpSaveData (optional)
            rotom_data: Rotom save data (size unknown, not detailed in header)
            style_data: Style save data (size unknown, not detailed in header)
        """
        accessor = cls()
        accessor.save_data = SaveData.from_bytes(player_data)

        if copy_dressup_data:
            accessor.copy_dressup_data = CopyDressUpSaveData.from_bytes(copy_dressup_data)

        # Note: rotom_data and style_data parsing would be implemented if we had their structures
        return accessor

    def to_bytes(self):
        """Convert to bytes for saving"""
        return {
            'player_data': self.save_data.to_bytes(),
            'copy_dressup_data': self.copy_dressup_data.to_bytes(),
            # rotom_data and style_data would be included here if we had their structures
        }

    def __str__(self):
        return f"PlayerSaveDataAccessor(\n  Main: {self.save_data}\n  Copy: {self.copy_dressup_data}\n)"
