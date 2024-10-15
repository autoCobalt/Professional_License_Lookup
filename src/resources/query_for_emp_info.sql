select
      a.emplid
    , a.first_name_srch
    , a.middle_name
    , a.last_name_srch
    , a.name_psformat
    , substr(nid.national_id, -4) last_4_ssn
    , p.city
    , p.state
    , p.postal
    , p.county
from
  ps_person_name a
  join ps_personal_data p on a.emplid = p.emplid
  left join ps_pers_nid nid on nid.emplid = a.emplid and nid.country = 'USA' and nid.national_id_type = 'PR'
where
  a.emplid in (&emplid_list)
order by
  a.emplid
;