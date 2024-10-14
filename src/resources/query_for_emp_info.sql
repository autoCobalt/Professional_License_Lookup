select
      a.emplid
    , a.first_name_srch
    , a.middle_name
    , a.last_name_srch
    , a.name_psformat
    , p.city
    , p.state
    , p.postal
    , p.county
from
  ps_person_name a
  join ps_personal_data p on a.emplid = p.emplid
where
  a.emplid in (&emplid_list)
order by
  a.emplid
;