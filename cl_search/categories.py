from cl_search.utils import selectors

VALID_CATEGORIES = {
    # community
    "community": f'{selectors["selectors"]["links"]["community"]["all"]}',
    "activities": f'{selectors["selectors"]["links"]["community"]["activities"]}',
    "artists": f'{selectors["selectors"]["links"]["community"]["artists"]}',
    "childcare": f'{selectors["selectors"]["links"]["community"]["childcare"]}',
    "classes": f'{selectors["selectors"]["links"]["community"]["classes"]}',
    "community events": f'{selectors["selectors"]["links"]["community"]["events"]}',
    "local events": f'{selectors["selectors"]["links"]["community"]["events"]}',
    "community general": f'{selectors["selectors"]["links"]["community"]["general"]}',
    "groups": f'{selectors["selectors"]["links"]["community"]["groups"]}',
    "local news": f'{selectors["selectors"]["links"]["community"]["local_news"]}',
    "news": f'{selectors["selectors"]["links"]["community"]["local_news"]}',
    "lost and found": f'{selectors["selectors"]["links"]["community"]["lost_found"]}',
    "missed connections": f'{selectors["selectors"]["links"]["community"]["missed_connections"]}',
    "musicians": f'{selectors["selectors"]["links"]["community"]["musicians"]}',
    "pets": f'{selectors["selectors"]["links"]["community"]["pets"]}',
    "politics": f'{selectors["selectors"]["links"]["community"]["politics"]}',
    "rants": f'{selectors["selectors"]["links"]["community"]["rants_raves"]}',
    "rideshare": f'{selectors["selectors"]["links"]["community"]["rideshare"]}',
    "volunteer": f'{selectors["selectors"]["links"]["community"]["volunteers"]}',
    # services
    "services": f'{selectors["selectors"]["links"]["services"]["all"]}',
    "automotive services": f'{selectors["selectors"]["links"]["services"]["automotive"]}',
    "beauty services": f'{selectors["selectors"]["links"]["services"]["beauty"]}',
    "cellphone services": f'{selectors["selectors"]["links"]["services"]["cell_mobile"]}',
    "computer services": f'{selectors["selectors"]["links"]["services"]["computer"]}',
    "creative services": f'{selectors["selectors"]["links"]["services"]["creative"]}',
    "cycling services": f'{selectors["selectors"]["links"]["services"]["cycle"]}',
    "event services": f'{selectors["selectors"]["links"]["services"]["event"]}',
    "farming services": f'{selectors["selectors"]["links"]["services"]["farm_garden"]}',
    "gardening services": f'{selectors["selectors"]["links"]["services"]["farm_garden"]}',
    "financial services": f'{selectors["selectors"]["links"]["services"]["financial"]}',
    "health services": f'{selectors["selectors"]["links"]["services"]["health_well"]}',
    "wellness services": f'{selectors["selectors"]["links"]["services"]["health_well"]}',
    "household services": f'{selectors["selectors"]["links"]["services"]["household"]}',
    "labor services": f'{selectors["selectors"]["links"]["services"]["labor_move"]}',
    "moving services": f'{selectors["selectors"]["links"]["services"]["labor_move"]}',
    "legal services": f'{selectors["selectors"]["links"]["services"]["legal"]}',
    "lessons": f'{selectors["selectors"]["links"]["services"]["lessons"]}',
    "marine services": f'{selectors["selectors"]["links"]["services"]["marine"]}',
    "pet services": f'{selectors["selectors"]["links"]["services"]["pet"]}',
    "real estate services": f'{selectors["selectors"]["links"]["services"]["real_estate"]}',
    "skilled services": f'{selectors["selectors"]["links"]["services"]["skilled_trade"]}',
    "small businesses": f'{selectors["selectors"]["links"]["services"]["sm_biz_ads"]}',
    "travel services": f'{selectors["selectors"]["links"]["services"]["travel_vac"]}',
    "vacation services": f'{selectors["selectors"]["links"]["services"]["travel_vac"]}',
    "writing services": f'{selectors["selectors"]["links"]["services"]["write_ed_tran"]}',
    "editing services": f'{selectors["selectors"]["links"]["services"]["write_ed_tran"]}',
    "translation": f'{selectors["selectors"]["links"]["services"]["write_ed_tran"]}',
    # housing
    "housing": f'{selectors["selectors"]["links"]["housing"]["all"]}',
    "apartements": f'{selectors["selectors"]["links"]["housing"]["apts_housing"]}',
    "houses": f'{selectors["selectors"]["links"]["housing"]["apts_housing"]}',
    "housing swap": f'{selectors["selectors"]["links"]["housing"]["housing_swap"]}',
    "housing wanted": f'{selectors["selectors"]["links"]["housing"]["housing_wanted"]}',
    "offices": f'{selectors["selectors"]["links"]["housing"]["office_commercial"]}',
    "commercial": f'{selectors["selectors"]["links"]["housing"]["office_commercial"]}',
    "parking": f'{selectors["selectors"]["links"]["housing"]["parking_storage"]}',
    "storage": f'{selectors["selectors"]["links"]["housing"]["parking_storage"]}',
    "real estate": f'{selectors["selectors"]["links"]["housing"]["for_sale"]}',
    "rooms": f'{selectors["selectors"]["links"]["housing"]["rooms_shared"]}',
    "shared houses": f'{selectors["selectors"]["links"]["housing"]["rooms_shared"]}',
    "rooms wanted": f'{selectors["selectors"]["links"]["housing"]["rooms_wanted"]}',
    "sublets": f'{selectors["selectors"]["links"]["housing"]["sublets_temporary"]}',
    "subleases": f'{selectors["selectors"]["links"]["housing"]["sublets_temporary"]}',
    "temporary housing": f'{selectors["selectors"]["links"]["housing"]["sublets_temporary"]}',
    "vacation rentals": f'{selectors["selectors"]["links"]["housing"]["vacation_rentals"]}',
    # for sale
    "sale": f'{selectors["selectors"]["links"]["for_sale"]["all"]}',
    "antiques": f'{selectors["selectors"]["links"]["for_sale"]["antiques"]}',
    "appliances": f'{selectors["selectors"]["links"]["for_sale"]["appliances"]}',
    "arts crafts": f'{selectors["selectors"]["links"]["for_sale"]["arts_crafts"]}',
    "crafts": f'{selectors["selectors"]["links"]["for_sale"]["arts_crafts"]}',
    "atvs": f'{selectors["selectors"]["links"]["for_sale"]["atv_utv_sno"]}',
    "atv": f'{selectors["selectors"]["links"]["for_sale"]["atv_utv_sno"]}',
    "utvs": f'{selectors["selectors"]["links"]["for_sale"]["atv_utv_sno"]}',
    "utv": f'{selectors["selectors"]["links"]["for_sale"]["atv_utv_sno"]}',
    "snowmobile": f'{selectors["selectors"]["links"]["for_sale"]["atv_utv_sno"]}',
    "snowmobiles": f'{selectors["selectors"]["links"]["for_sale"]["atv_utv_sno"]}',
    "auto parts": f'{selectors["selectors"]["links"]["for_sale"]["auto_parts"]}',
    "aviation": f'{selectors["selectors"]["links"]["for_sale"]["aviation"]}',
    "airplanes": f'{selectors["selectors"]["links"]["for_sale"]["aviation"]}',
    "baby": f'{selectors["selectors"]["links"]["for_sale"]["baby_kid"]}',
    "babies": f'{selectors["selectors"]["links"]["for_sale"]["baby_kid"]}',
    "kids": f'{selectors["selectors"]["links"]["for_sale"]["baby_kid"]}',
    "barter": f'{selectors["selectors"]["links"]["for_sale"]["barter"]}',
    "beauty": f'{selectors["selectors"]["links"]["for_sale"]["beauty_health"]}',
    "makeup": f'{selectors["selectors"]["links"]["for_sale"]["beauty_health"]}',
    "health": f'{selectors["selectors"]["links"]["for_sale"]["beauty_health"]}',
    "bike parts": f'{selectors["selectors"]["links"]["for_sale"]["bike_parts"]}',
    "bikes": f'{selectors["selectors"]["links"]["for_sale"]["bikes"]}',
    "boat parts": f'{selectors["selectors"]["links"]["for_sale"]["boat_parts"]}',
    "boats": f'{selectors["selectors"]["links"]["for_sale"]["boats"]}',
    "books": f'{selectors["selectors"]["links"]["for_sale"]["books"]}',
    "business": f'{selectors["selectors"]["links"]["for_sale"]["business"]}',
    "cars": f'{selectors["selectors"]["links"]["for_sale"]["cars_trucks"]}',
    "trucks": f'{selectors["selectors"]["links"]["for_sale"]["cars_trucks"]}',
    "cds": f'{selectors["selectors"]["links"]["for_sale"]["cds_dvd_vhs"]}',
    "dvds": f'{selectors["selectors"]["links"]["for_sale"]["cds_dvd_vhs"]}',
    "vhs": f'{selectors["selectors"]["links"]["for_sale"]["cds_dvd_vhs"]}',
    "cellphones": f'{selectors["selectors"]["links"]["for_sale"]["cell_phones"]}',
    "clothes": f'{selectors["selectors"]["links"]["for_sale"]["clothes_acc"]}',
    "accessories": f'{selectors["selectors"]["links"]["for_sale"]["clothes_acc"]}',
    "collectibles": f'{selectors["selectors"]["links"]["for_sale"]["collectibles"]}',
    "computer parts": f'{selectors["selectors"]["links"]["for_sale"]["computer_parts"]}',
    "computers": f'{selectors["selectors"]["links"]["for_sale"]["computers"]}',
    "electronics": f'{selectors["selectors"]["links"]["for_sale"]["electronics"]}',
    "farm": f'{selectors["selectors"]["links"]["for_sale"]["farm_garden"]}',
    "garden": f'{selectors["selectors"]["links"]["for_sale"]["farm_garden"]}',
    "free": f'{selectors["selectors"]["links"]["for_sale"]["free"]}',
    "furniture": f'{selectors["selectors"]["links"]["for_sale"]["furniture"]}',
    "garage sale": f'{selectors["selectors"]["links"]["for_sale"]["garage_sale"]}',
    "general": f'{selectors["selectors"]["links"]["for_sale"]["general"]}',
    "heavy eqiupment": f'{selectors["selectors"]["links"]["for_sale"]["heavy_equip"]}',
    "household goods": f'{selectors["selectors"]["links"]["for_sale"]["household"]}',
    "jewelry": f'{selectors["selectors"]["links"]["for_sale"]["jewelry"]}',
    "materials": f'{selectors["selectors"]["links"]["for_sale"]["materials"]}',
    "motorcycle parts": f'{selectors["selectors"]["links"]["for_sale"]["motorcycle_parts"]}',
    "motorcycles": f'{selectors["selectors"]["links"]["for_sale"]["motorcycles"]}',
    "music instruments": f'{selectors["selectors"]["links"]["for_sale"]["music_instr"]}',
    "photography gear": f'{selectors["selectors"]["links"]["for_sale"]["photo_video"]}',
    "video gear": f'{selectors["selectors"]["links"]["for_sale"]["photo_video"]}',
    "rvs": f'{selectors["selectors"]["links"]["for_sale"]["rvs_camp"]}',
    "campers": f'{selectors["selectors"]["links"]["for_sale"]["rvs_camp"]}',
    "sports": f'{selectors["selectors"]["links"]["for_sale"]["sporting"]}',
    "tickets": f'{selectors["selectors"]["links"]["for_sale"]["tickets"]}',
    "tools": f'{selectors["selectors"]["links"]["for_sale"]["tools"]}',
    "toys": f'{selectors["selectors"]["links"]["for_sale"]["toys_games"]}',
    "games": f'{selectors["selectors"]["links"]["for_sale"]["toys_games"]}',
    "trailers": f'{selectors["selectors"]["links"]["for_sale"]["trailers"]}',
    "video games": f'{selectors["selectors"]["links"]["for_sale"]["video_gaming"]}',
    "wanted": f'{selectors["selectors"]["links"]["for_sale"]["wanted"]}',
    "wheels": f'{selectors["selectors"]["links"]["for_sale"]["wheels_tires"]}',
    "tires": f'{selectors["selectors"]["links"]["for_sale"]["wheels_tires"]}',
    # jobs
    "jobs": f'{selectors["selectors"]["links"]["jobs"]["all"]}',
    "accounting": f'{selectors["selectors"]["links"]["jobs"]["accounting"]}',
    "accounting jobs": f'{selectors["selectors"]["links"]["jobs"]["accounting"]}',
    "finance": f'{selectors["selectors"]["links"]["jobs"]["accounting"]}',
    "finance jobs": f'{selectors["selectors"]["links"]["jobs"]["accounting"]}',
    "admin": f'{selectors["selectors"]["links"]["jobs"]["admin_office"]}',
    "admin jobs": f'{selectors["selectors"]["links"]["jobs"]["admin_office"]}',
    "office jobs": f'{selectors["selectors"]["links"]["jobs"]["admin_office"]}',
    "architecture": f'{selectors["selectors"]["links"]["jobs"]["arch_engineering"]}',
    "engineering": f'{selectors["selectors"]["links"]["jobs"]["arch_engineering"]}',
    "art": f'{selectors["selectors"]["links"]["jobs"]["art_media_design"]}',
    "art jobs": f'{selectors["selectors"]["links"]["jobs"]["art_media_design"]}',
    "media": f'{selectors["selectors"]["links"]["jobs"]["art_media_design"]}',
    "media jobs": f'{selectors["selectors"]["links"]["jobs"]["art_media_design"]}',
    "design": f'{selectors["selectors"]["links"]["jobs"]["art_media_design"]}',
    "design jobs": f'{selectors["selectors"]["links"]["jobs"]["art_media_design"]}',
    "graphic design": f'{selectors["selectors"]["links"]["jobs"]["art_media_design"]}',
    "graphic design jobs": f'{selectors["selectors"]["links"]["jobs"]["art_media_design"]}',
    "biotech": f'{selectors["selectors"]["links"]["jobs"]["biotech_science"]}',
    "biotech jobs": f'{selectors["selectors"]["links"]["jobs"]["biotech_science"]}',
    "science": f'{selectors["selectors"]["links"]["jobs"]["biotech_science"]}',
    "science jobs": f'{selectors["selectors"]["links"]["jobs"]["biotech_science"]}',
    "business management": f'{selectors["selectors"]["links"]["jobs"]["business_mgmt"]}',
    "management": f'{selectors["selectors"]["links"]["jobs"]["business_mgmt"]}',
    "mgmt": f'{selectors["selectors"]["links"]["jobs"]["business_mgmt"]}',
    "customer service": f'{selectors["selectors"]["links"]["jobs"]["customer_service"]}',
    "cs": f'{selectors["selectors"]["links"]["jobs"]["customer_service"]}',
    "education": f'{selectors["selectors"]["links"]["jobs"]["education"]}',
    "teaching": f'{selectors["selectors"]["links"]["jobs"]["education"]}',
    "other jobs": f'{selectors["selectors"]["links"]["jobs"]["etc_misc"]}',
    "food": f'{selectors["selectors"]["links"]["jobs"]["food_bev_hosp"]}',
    "beverage": f'{selectors["selectors"]["links"]["jobs"]["food_bev_hosp"]}',
    "hospitality": f'{selectors["selectors"]["links"]["jobs"]["food_bev_hosp"]}',
    "restaurant": f'{selectors["selectors"]["links"]["jobs"]["food_bev_hosp"]}',
    "general labor": f'{selectors["selectors"]["links"]["jobs"]["general_labor"]}',
    "government": f'{selectors["selectors"]["links"]["jobs"]["government"]}',
    "gov": f'{selectors["selectors"]["links"]["jobs"]["government"]}',
    "government jobs": f'{selectors["selectors"]["links"]["jobs"]["government"]}',
    "hr": f'{selectors["selectors"]["links"]["jobs"]["hr"]}',
    "human resources": f'{selectors["selectors"]["links"]["jobs"]["hr"]}',
    "legal": f'{selectors["selectors"]["links"]["jobs"]["legal"]}',
    "legal jobs": f'{selectors["selectors"]["links"]["jobs"]["legal"]}',
    "paralegal": f'{selectors["selectors"]["links"]["jobs"]["legal"]}',
    "manufacturing": f'{selectors["selectors"]["links"]["jobs"]["manufacturing"]}',
    "manufacturing jobs": f'{selectors["selectors"]["links"]["jobs"]["manufacturing"]}',
    "marketing": f'{selectors["selectors"]["links"]["jobs"]["marketing"]}',
    "marketing jobs": f'{selectors["selectors"]["links"]["jobs"]["marketing"]}',
    "advertising": f'{selectors["selectors"]["links"]["jobs"]["marketing"]}',
    "advertising jobs": f'{selectors["selectors"]["links"]["jobs"]["marketing"]}',
    "pr": f'{selectors["selectors"]["links"]["jobs"]["marketing"]}',
    "public relations": f'{selectors["selectors"]["links"]["jobs"]["marketing"]}',
    "pr jobs": f'{selectors["selectors"]["links"]["jobs"]["marketing"]}',
    "medical": f'{selectors["selectors"]["links"]["jobs"]["medical_health"]}',
    "medical jobs": f'{selectors["selectors"]["links"]["jobs"]["medical_health"]}',
    "health jobs": f'{selectors["selectors"]["links"]["jobs"]["medical_health"]}',
    "doctors": f'{selectors["selectors"]["links"]["jobs"]["medical_health"]}',
    "nursing": f'{selectors["selectors"]["links"]["jobs"]["medical_health"]}',
    "nonprofit": f'{selectors["selectors"]["links"]["jobs"]["nonprofit"]}',
    "nonprofits": f'{selectors["selectors"]["links"]["jobs"]["nonprofit"]}',
    "ngo": f'{selectors["selectors"]["links"]["jobs"]["nonprofit"]}',
    "nonprofit jobs": f'{selectors["selectors"]["links"]["jobs"]["nonprofit"]}',
    "real estate jobs": f'{selectors["selectors"]["links"]["jobs"]["real_estate"]}',
    "retail": f'{selectors["selectors"]["links"]["jobs"]["retail"]}',
    "retail jobs": f'{selectors["selectors"]["links"]["jobs"]["retail"]}',
    "wholesale": f'{selectors["selectors"]["links"]["jobs"]["retail"]}',
    "wholesale jobs": f'{selectors["selectors"]["links"]["jobs"]["retail"]}',
    "sales": f'{selectors["selectors"]["links"]["jobs"]["sales"]}',
    "sales jobs": f'{selectors["selectors"]["links"]["jobs"]["sales"]}',
    "business development": f'{selectors["selectors"]["links"]["jobs"]["sales"]}',
    "bd": f'{selectors["selectors"]["links"]["jobs"]["sales"]}',
    "bdr": f'{selectors["selectors"]["links"]["jobs"]["sales"]}',
    "business development jobs": f'{selectors["selectors"]["links"]["jobs"]["sales"]}',
    "salon": f'{selectors["selectors"]["links"]["jobs"]["salon_fitness"]}',
    "spa": f'{selectors["selectors"]["links"]["jobs"]["salon_fitness"]}',
    "fitness": f'{selectors["selectors"]["links"]["jobs"]["salon_fitness"]}',
    "fitness instructor": f'{selectors["selectors"]["links"]["jobs"]["salon_fitness"]}',
    "security": f'{selectors["selectors"]["links"]["jobs"]["security"]}',
    "trades": f'{selectors["selectors"]["links"]["jobs"]["skilled_trade"]}',
    "trade jobs": f'{selectors["selectors"]["links"]["jobs"]["skilled_trade"]}',
    "blue collar": f'{selectors["selectors"]["links"]["jobs"]["skilled_trade"]}',
    "blue collar jobs": f'{selectors["selectors"]["links"]["jobs"]["skilled_trade"]}',
    "software": f'{selectors["selectors"]["links"]["jobs"]["software"]}',
    "software jobs": f'{selectors["selectors"]["links"]["jobs"]["software"]}',
    "qa": f'{selectors["selectors"]["links"]["jobs"]["software"]}',
    "qa jobs": f'{selectors["selectors"]["links"]["jobs"]["software"]}',
    "dba": f'{selectors["selectors"]["links"]["jobs"]["software"]}',
    "dba jobs": f'{selectors["selectors"]["links"]["jobs"]["software"]}',
    "systems": f'{selectors["selectors"]["links"]["jobs"]["systems_network"]}',
    "system jobs": f'{selectors["selectors"]["links"]["jobs"]["systems_network"]}',
    "it": f'{selectors["selectors"]["links"]["jobs"]["systems_network"]}',
    "it jobs": f'{selectors["selectors"]["links"]["jobs"]["systems_network"]}',
    "networking": f'{selectors["selectors"]["links"]["jobs"]["systems_network"]}',
    "tech support": f'{selectors["selectors"]["links"]["jobs"]["technical_support"]}',
    "technical support": f'{selectors["selectors"]["links"]["jobs"]["technical_support"]}',
    "transportation": f'{selectors["selectors"]["links"]["jobs"]["transport"]}',
    "transport": f'{selectors["selectors"]["links"]["jobs"]["transport"]}',
    "trucking": f'{selectors["selectors"]["links"]["jobs"]["transport"]}',
    "tv": f'{selectors["selectors"]["links"]["jobs"]["tv_film_video"]}',
    "television": f'{selectors["selectors"]["links"]["jobs"]["tv_film_video"]}',
    "film": f'{selectors["selectors"]["links"]["jobs"]["tv_film_video"]}',
    "video": f'{selectors["selectors"]["links"]["jobs"]["tv_film_video"]}',
    "web design": f'{selectors["selectors"]["links"]["jobs"]["web_info_design"]}',
    "info design": f'{selectors["selectors"]["links"]["jobs"]["web_info_design"]}',
    "writers": f'{selectors["selectors"]["links"]["jobs"]["writing_editing"]}',
    "creative writing": f'{selectors["selectors"]["links"]["jobs"]["writing_editing"]}',
    "writing": f'{selectors["selectors"]["links"]["jobs"]["writing_editing"]}',
    "editors": f'{selectors["selectors"]["links"]["jobs"]["writing_editing"]}',
    "editing": f'{selectors["selectors"]["links"]["jobs"]["writing_editing"]}',
    "video editing": f'{selectors["selectors"]["links"]["jobs"]["writing_editing"]}',
    # gigs
    "gigs": f'{selectors["selectors"]["links"]["gigs"]["all"]}',
    "computer gigs": f'{selectors["selectors"]["links"]["gigs"]["computer"]}',
    "creative gigs": f'{selectors["selectors"]["links"]["gigs"]["creative"]}',
    "creative": f'{selectors["selectors"]["links"]["gigs"]["creative"]}',
    "crew": f'{selectors["selectors"]["links"]["gigs"]["crew"]}',
    "crew gigs": f'{selectors["selectors"]["links"]["gigs"]["crew"]}',
    "domestic": f'{selectors["selectors"]["links"]["gigs"]["domestic"]}',
    "domestic gigs": f'{selectors["selectors"]["links"]["gigs"]["domestic"]}',
    "housekeeping": f'{selectors["selectors"]["links"]["gigs"]["domestic"]}',
    "handyman": f'{selectors["selectors"]["links"]["gigs"]["domestic"]}',
    "event gigs": f'{selectors["selectors"]["links"]["gigs"]["event"]}',
    "labor gigs": f'{selectors["selectors"]["links"]["gigs"]["labor"]}',
    "helpers": f'{selectors["selectors"]["links"]["gigs"]["labor"]}',
    "talent": f'{selectors["selectors"]["links"]["gigs"]["talent"]}',
    "writing gigs": f'{selectors["selectors"]["links"]["gigs"]["writing"]}',
    # resumes
    "resumes": f'{selectors["selectors"]["links"]["resumes"]}',
    "resume": f'{selectors["selectors"]["links"]["resumes"]}',
    # event calendar
    "events": f'{selectors["selectors"]["links"]["event_calendar"]}',
    "event calendar": f'{selectors["selectors"]["links"]["event_calendar"]}',
}
