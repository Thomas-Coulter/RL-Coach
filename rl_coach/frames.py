"""Turns parsed rrrocket/boxcars JSON into a tidy per-frame DataFrame of rigid body state.

Actor IDs are reused throughout a replay as objects spawn and despawn (e.g. a car
actor_id gets freed on disconnect and reassigned to a different car later), so we
track each actor's current class name live as we walk frames in order rather than
building a single static actor_id -> class mapping.
"""

import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation


def rigid_body_dataframe(replay_json: dict) -> pd.DataFrame:
    """Flatten network_frames RigidBody updates into one row per actor per frame.

    Only rows for actors that received a RigidBody update on that frame are
    emitted (the network stream is delta-compressed - most actors don't update
    every frame). Resample/forward-fill per actor_id downstream if you need a
    dense per-frame table.
    """
    objects = replay_json["objects"]
    frames = replay_json["network_frames"]["frames"]

    live_class: dict[int, str] = {}
    rows = []

    for frame_idx, frame in enumerate(frames):
        for new_actor in frame["new_actors"]:
            live_class[new_actor["actor_id"]] = objects[new_actor["object_id"]]

        for updated in frame["updated_actors"]:
            attr = updated["attribute"]
            if not isinstance(attr, dict) or "RigidBody" not in attr:
                continue
            rb = attr["RigidBody"]
            loc = rb["location"]
            rot = rb["rotation"]
            lin_vel = rb["linear_velocity"] or {}
            ang_vel = rb["angular_velocity"] or {}

            rows.append(
                {
                    "frame": frame_idx,
                    "time": frame["time"],
                    "actor_id": updated["actor_id"],
                    "class": live_class.get(updated["actor_id"]),
                    "sleeping": rb["sleeping"],
                    "x": loc["x"],
                    "y": loc["y"],
                    "z": loc["z"],
                    "rot_x": rot.get("x"),
                    "rot_y": rot.get("y"),
                    "rot_z": rot.get("z"),
                    "rot_w": rot.get("w"),
                    "vx": lin_vel.get("x"),
                    "vy": lin_vel.get("y"),
                    "vz": lin_vel.get("z"),
                    "ang_x": ang_vel.get("x"),
                    "ang_y": ang_vel.get("y"),
                    "ang_z": ang_vel.get("z"),
                }
            )

        for deleted_id in frame["deleted_actors"]:
            live_class.pop(deleted_id, None)

    return pd.DataFrame(rows)


def add_orientation_vectors(df: pd.DataFrame) -> pd.DataFrame:
    """Add forward/right/up unit vectors derived from the rotation quaternion.

    Uses scipy's Rotation with RL's convention that a car's local forward axis
    is +X, right is +Y, up is +Z before rotation is applied.
    """
    quat_cols = ["rot_x", "rot_y", "rot_z", "rot_w"]
    mask = df[quat_cols].notna().all(axis=1)

    forward = np.full((len(df), 3), np.nan)
    right = np.full((len(df), 3), np.nan)
    up = np.full((len(df), 3), np.nan)

    if mask.any():
        rotations = Rotation.from_quat(df.loc[mask, quat_cols].to_numpy())
        forward[mask.to_numpy()] = rotations.apply([1, 0, 0])
        right[mask.to_numpy()] = rotations.apply([0, 1, 0])
        up[mask.to_numpy()] = rotations.apply([0, 0, 1])

    out = df.copy()
    out[["forward_x", "forward_y", "forward_z"]] = forward
    out[["right_x", "right_y", "right_z"]] = right
    out[["up_x", "up_y", "up_z"]] = up
    return out
