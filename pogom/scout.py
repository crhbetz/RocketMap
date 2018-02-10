import logging
import sys

import requests
from base64 import b64encode

from .utils import get_pokemon_name

log = logging.getLogger("Scout")

scout_url = "http://127.0.0.1:4243/iv";

def scout_error(error_msg):
    log.error(error_msg)
    return {
        "success": False,
        "error": error_msg
    }


def pgscout_encounter(p):
    # Assemble PGScout request
    params = {
        'pokemon_id': p.pokemon_id,
        'encounter_id': p.encounter_id,
        'spawn_point_id': p.spawnpoint_id,
        'latitude': p.latitude,
        'longitude': p.longitude
    }
    try:
        r = requests.get(scout_url, params=params)
    except:
        return scout_error(
            "Exception on scout: {}".format(repr(sys.exc_info()[1])))

    return r.json() if r.status_code == 200 else scout_error(
        "Got error {} from scout service.".format(r.status_code))


def encounter_pokemon_scout(args, p, account, api, account_sets, status, key_scheduler):
    pokemon_id = p.pokemon_data.pokemon_id
    pokemon_name = get_pokemon_name(pokemon_id)
    log.info(u"Scouting {} at {}, {}.".format(pokemon_name, p.latitude,
                                                  p.longitude))

    # Prepare Pokemon object
    pkm = type('', (), {})()
    pkm.pokemon_id = pokemon_id
    pkm.encounter_id = b64encode(str(p.encounter_id))
    pkm.spawnpoint_id = p.spawn_point_id
    pkm.latitude = p.latitude
    pkm.longitude = p.longitude
    scout_result = pgscout_encounter(pkm)
    if scout_result['success']:
        log.info(
            u"Successfully Scouted a {:.1f}% lvl {} {} with {} CP"
            u" (scout level {}).".format(
                scout_result['iv_percent'], scout_result['level'],
                pokemon_name, scout_result['cp'], scout_result['scout_level']))
    else:
        log.warning(u"Failed Scouting {}: {}".format(pokemon_name,
                                                       scout_result['error']))
        return False
    #change to the same format as the normal encounter is expecting
    result = type('', (), {})()
    result.individual_attack = scout_result['iv_attack']
    result.individual_defense = scout_result['iv_defense']
    result.individual_stamina = scout_result['iv_stamina']
    result.move_1 = scout_result['move_1']
    result.move_2 = scout_result['move_2']
    result.height_m = scout_result['height']
    result.weight_kg = scout_result['weight']
    result.cp = scout_result['cp']
    result.cp_multiplier = scout_result['cp_multiplier']
    return result
