local parking = redis.call("get", KEYS[1])
if parking then return parking end
local free_parking = redis.call("lpop", "fp") 
-- fp is list holding free parking spaces
-- It would probably be better placed as a key provided to this script
if free_parking == nil then return 'Invalid, out of parking' end
redis.call("set", KEYS[1], free_parking)
return free_parking