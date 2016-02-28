REFRESH MATERIALIZED VIEW einwohner.view_b1_m_all_buildings;
REFRESH MATERIALIZED VIEW einwohner.view_g_m_buildings_ewsynth_alkl;
REFRESH MATERIALIZED VIEW einwohner.view_i03_m_building_ewsynth_alkl_nach_abgleich_mit_statbez;
REFRESH MATERIALIZED VIEW landuse.matview_erholungsflaeche;
REFRESH MATERIALIZED VIEW raumeinheiten."progbez_of_baublock" ;
REFRESH MATERIALIZED VIEW einwohner.view_j_m_ew2015_alkl_baublhan;
REFRESH MATERIALIZED VIEW einwohner.view_j_m_ew2015_alkl_geb_umland;
REFRESH MATERIALIZED VIEW randsummen.matview_randsumme_arbeitsplaetze_2015_long;
REFRESH MATERIALIZED VIEW apl.matview_alle_betriebe;
REFRESH MATERIALIZED VIEW apl.matview_apl_mit_rsa;
REFRESH MATERIALIZED VIEW strukturdaten.matview_pgr_alkl_gebtyp;

SET SESSION AUTHORIZATION verkehr;
DROP VIEW verkehrszellen.view_vz_aktuell CASCADE;
DROP TABLE IF EXISTS strukturdaten.vz_apl_wz_bereiche;
DROP TABLE IF EXISTS strukturdaten.vz_handel;
DROP TABLE IF EXISTS strukturdaten.vz_zielpotenziel_aktivitaeten;
CREATE OR REPLACE VIEW verkehrszellen.view_vz_aktuell(
    id,
    geom,
    zone_name)
AS
  SELECT t.gid AS id,
         t.geom::geometry(GEOMETRY),
         t.gid::text AS zone_name
  FROM verkehrszellen.garmi t;

CREATE VIEW einwohner.view_l_vz_ew_alkl_2015 (
    vz_id,
    alkl_id,
    alkl,
    einw)
AS
SELECT vz.id AS vz_id,
    e.alkl_id,
    a.alkl,
    sum(e.einw) AS einw
FROM verkehrszellen.view_vz_aktuell vz
   LEFT JOIN (
    SELECT ant.id AS vz_id,
                    ew_h.alkl_id,
                    ew_h.ew * ant.anteil AS einw
    FROM einwohner.view_j_m_ew2015_alkl_baublhan ew_h,
                    _raumeinheiten._vz_skh5_baubloecke ant
    WHERE ew_h.baubloecke = ant.baubloecke::text
    UNION ALL
    SELECT ant.id AS vz_id,
                    ew_u.alkl_id,
                    ew_u.ew * ant.anteil AS einw
    FROM einwohner.view_j_m_ew2015_alkl_geb_umland ew_u,
                    _einwohner._vz_view_b1_m_all_buildings ant
    WHERE ew_u.building_id = ant.building_id
    ) e ON vz.id::double precision = e.vz_id::double precision,
    einwohner.altersklassen a
WHERE e.alkl_id = a.alkl_id
GROUP BY vz.id, e.alkl_id, a.alkl;

CREATE MATERIALIZED VIEW einwohner.view_l_m_vz_ew_alkl_2015(
    vz_id,
    alkl_id,
    alkl,
    einw)
AS
  SELECT view_l_vz_ew_alkl_2015.vz_id,
         view_l_vz_ew_alkl_2015.alkl_id,
         view_l_vz_ew_alkl_2015.alkl,
         view_l_vz_ew_alkl_2015.einw
  FROM einwohner.view_l_vz_ew_alkl_2015;

CREATE OR REPLACE VIEW verkehrszellen.view_vz_progbez(
    vz_id,
    progbez_id)
AS
  SELECT v.id AS vz_id,
         COALESCE(p.id::integer, (- 1)) AS progbez_id
  FROM verkehrszellen.view_vz_aktuell v
       LEFT JOIN raumeinheiten.prognosebezirke p ON st_within(st_pointonsurface(
         v.geom), p.geom);
		 
CREATE MATERIALIZED VIEW verkehrszellen.mview_vz_progbez(
    vz_id,
    progbez_id)
AS
  SELECT view_vz_progbez.vz_id,
         view_vz_progbez.progbez_id
  FROM verkehrszellen.view_vz_progbez;

  
		 
		 
		 
CREATE OR REPLACE VIEW einwohner.view_l1_progbez_einw_alkl_2015(
    progbez_id,
    alkl_id,
    einw)
AS
  SELECT vp.progbez_id,
         e.alkl_id,
         sum(e.einw) AS einw
  FROM einwohner.view_l_m_vz_ew_alkl_2015 e,
       verkehrszellen.mview_vz_progbez vp
  WHERE e.vz_id = vp.vz_id
  GROUP BY vp.progbez_id,
           e.alkl_id;
		   
CREATE OR REPLACE VIEW planungen.view_vz_neubau_ew_alkl(
    progbez_id,
    vz_id,
    alkl_id,
    einw)
AS
  SELECT vp.progbez_id,
         nv.vz_id,
         n_1.alkl_id,
         sum(n_1.ew * nv.anteil) AS einw
  FROM planungen.siedlung_jahr_alkl n_1,
       planungen.neubau_vz nv,
       verkehrszellen.mview_vz_progbez vp
  WHERE n_1.id::numeric = nv.id AND
        vp.vz_id = nv.vz_id AND
        nv.area = n_1.area
  GROUP BY vp.progbez_id,
           nv.vz_id,
           n_1.alkl_id;

CREATE OR REPLACE VIEW planungen.neubau_progbez_alkl(
    progbez_id,
    alkl_id,
    ew)
AS
  SELECT vp.progbez_id,
         s.alkl_id,
         sum(s.ew * r.anteil) AS ew
  FROM planungen.siedlung_jahr_alkl s,
       planungen.neubau_vz r,
       verkehrszellen.mview_vz_progbez vp
  WHERE r.vz_id = vp.vz_id AND
        s.id::numeric = r.id AND
        s.area = r.area
  GROUP BY vp.progbez_id,
           s.alkl_id;

CREATE OR REPLACE VIEW einwohner.view_l3_kf_neubau_prognose(
    progbez_id,
    alkl_id,
    kf,
    ew_soll,
    ew_alt,
    ew_neubau)
AS
  SELECT p.id AS progbez_id,
         s.alkl_id,
         CASE
           WHEN (COALESCE(a.einw, 0::double precision) + COALESCE(n.ew, 0::
             double precision)) = 0::double precision THEN 1::double precision
           ELSE s.ew_soll /(COALESCE(a.einw, 0::double precision) + COALESCE(
             n.ew, 0::double precision))
         END AS kf,
         s.ew_soll,
         a.einw AS ew_alt,
         n.ew AS ew_neubau
  FROM einwohner.view_i1_ewsoll_prognosejahr_alkl_progbez s
       JOIN raumeinheiten.prognosebezirke p ON s.gem_id = p.gem_id
       LEFT JOIN planungen.neubau_progbez_alkl n ON p.id = n.progbez_id AND
         s.alkl_id = n.alkl_id
       LEFT JOIN einwohner.view_l1_progbez_einw_alkl_2015 a ON p.id =
         a.progbez_id AND s.alkl_id = a.alkl_id;

CREATE OR REPLACE VIEW einwohner.view_l2_vz_ew_alkl_prognosejahr(
    vz_id,
    alkl_id,
    alkl,
    einw)
AS
  SELECT v.id AS vz_id,
         a.alkl_id,
         a.alkl,
         COALESCE(e.einw, 0::double precision) + COALESCE(n.einw, 0::double
           precision) AS einw
  FROM verkehrszellen.view_vz_aktuell v
       CROSS JOIN einwohner.altersklassen a
       LEFT JOIN einwohner.view_l_m_vz_ew_alkl_2015 e ON v.id = e.vz_id AND
         a.alkl_id = e.alkl_id
       LEFT JOIN planungen.view_vz_neubau_ew_alkl n ON v.id = n.vz_id AND
         a.alkl_id = n.alkl_id;

CREATE OR REPLACE VIEW einwohner.view_l4_vz_ew_alkl_prognosejahr(
    vz_id,
    alkl_id,
    alkl,
    einw)
AS
  SELECT e.vz_id,
         e.alkl_id,
         e.alkl,
         e.einw * kf.kf AS einw
  FROM einwohner.view_l2_vz_ew_alkl_prognosejahr e,
       einwohner.view_l3_kf_neubau_prognose kf,
       verkehrszellen.mview_vz_progbez vp
  WHERE e.vz_id = vp.vz_id AND
        vp.progbez_id = kf.progbez_id AND
        e.alkl_id = kf.alkl_id;

CREATE OR REPLACE VIEW einwohner.view_k_kontrolle_prognosejahr_alkl(
    progbez_id,
    alkl_id,
    ew_ist,
    ew_soll)
AS
  SELECT p.id AS progbez_id,
         s.alkl_id,
         i.ew_ist,
         s.ew_soll
  FROM einwohner.view_i1_ewsoll_prognosejahr_alkl_progbez s,
       raumeinheiten.prognosebezirke p,
       (
         SELECT vp.progbez_id,
                i_1.alkl_id,
                sum(i_1.einw) AS ew_ist
         FROM einwohner.view_l4_vz_ew_alkl_prognosejahr i_1,
              verkehrszellen.mview_vz_progbez vp
         WHERE i_1.vz_id = vp.vz_id
         GROUP BY vp.progbez_id,
                  i_1.alkl_id
         ORDER BY vp.progbez_id,
                  i_1.alkl_id
       ) i
  WHERE i.alkl_id = s.alkl_id AND
        p.gem_id = s.gem_id AND
        p.id = i.progbez_id;



CREATE MATERIALIZED VIEW verkehrszellen.matview_vzaktuell_centroids 
AS 
SELECT id, st_pointonsurface(v.geom) AS geom
FROM verkehrszellen.view_vz_aktuell v;
CREATE INDEX matview_vzaktuell_centroids_geom_idx ON verkehrszellen.matview_vzaktuell_centroids 
USING gist(geom);


CREATE OR REPLACE VIEW verkehrszellen.vz_aktuell_gebietstypen AS 
 SELECT v.id, 
    z.typeno, 
    COALESCE(s.an_schiene, 0::smallint) AS anschiene, 
    e.faktor_eink
   FROM    verkehrszellen.view_vz_aktuell v
   LEFT JOIN verkehrszellen.matview_vzaktuell_centroids c ON v.id=c.id
   LEFT JOIN verkehrszellen.vz_aktuell_buffer_schiene s ON st_intersects(c.geom, s.geom) , 
    verkehrszellen.faktor_einkauf e, 
    verkehrszellen.zentralitaet z
  WHERE st_intersects(c.geom, z.geom) AND st_intersects(c.geom, e.geom) ;


CREATE MATERIALIZED VIEW verkehrszellen.matview_vz_aktuell_gebietstypen(
    id,
    typeno,
    anschiene,
    faktor_eink)
AS
  SELECT vz_aktuell_gebietstypen.id,
         vz_aktuell_gebietstypen.typeno,
         vz_aktuell_gebietstypen.anschiene,
         vz_aktuell_gebietstypen.faktor_eink
  FROM verkehrszellen.vz_aktuell_gebietstypen;

CREATE OR REPLACE VIEW einwohner.vz_personengruppen_2015(
    vz_id,
    pgr,
    einw)
AS
  SELECT ew.vz_id,
         pg.pgr,
         sum(pg.anteil * ew.einw) AS einw
  FROM einwohner.view_l_m_vz_ew_alkl_2015 ew,
       strukturdaten.pgr_anteile_current_year pg,
       verkehrszellen.view_vz_aktuell vz,
       verkehrszellen.matview_vz_aktuell_gebietstypen gt
  WHERE ew.alkl_id = pg.alkl_id AND
        ew.vz_id = vz.id AND
        vz.id = gt.id AND
        gt.typeno = pg.gebtyp AND
        gt.anschiene = pg.an_schiene
  GROUP BY ew.vz_id,
           pg.pgr
  ORDER BY ew.vz_id,
           pg.pgr;

REFRESH MATERIALIZED VIEW verkehrszellen.matview_vz_aktuell_gebietstypen;

     	   
CREATE OR REPLACE VIEW einwohner.vz_personengruppen_prognosejahr(
    vz_id,
    pgr,
    einw)
AS
  SELECT ew.vz_id,
         pg.pgr,
         sum(pg.anteil * ew.einw) AS einw
  FROM einwohner.view_l4_vz_ew_alkl_prognosejahr ew,
       strukturdaten.pgr_anteile_current_year pg,
       verkehrszellen.view_vz_aktuell vz,
       verkehrszellen.matview_vz_aktuell_gebietstypen gt
  WHERE ew.alkl_id = pg.alkl_id AND
        ew.vz_id = vz.id AND
        vz.id = gt.id AND
        gt.typeno = pg.gebtyp AND
        gt.anschiene = pg.an_schiene
  GROUP BY ew.vz_id,
           pg.pgr
  ORDER BY ew.vz_id,
           pg.pgr;

CREATE OR REPLACE VIEW strukturdaten.vz_bildung(
    vz_id,
    gs,
    sek_1,
    sek_2,
    foerderschueler,
    sek12,
    bs,
    bbs_vz,
    bbs_tz,
    studierende,
    betreuungsplaetze)
AS
  SELECT v.id AS vz_id,
         COALESCE(s.gs, 0::double precision) AS gs,
         COALESCE(s.sek_1, 0::double precision) AS sek_1,
         COALESCE(s.sek_2, 0::double precision) AS sek_2,
         COALESCE(s.foerderschu, 0::double precision) AS foerderschueler,
         COALESCE(s.sek12, 0::double precision) AS sek12,
         COALESCE(s.bs, 0::double precision) AS bs,
         COALESCE(s.bbs_vz, 0::double precision) AS bbs_vz,
         COALESCE(s.bbs_tz, 0::double precision) AS bbs_tz,
         COALESCE(h.studierende, 0::double precision) AS studierende,
         COALESCE(k.betreuungsplaetze, 0::double precision) AS betreuungsplaetze
  FROM verkehrszellen.view_vz_aktuell v
       LEFT JOIN 
       (
         SELECT vs.id_zone AS vz_id,
                sum(s_1.gs::double precision * vs.anteil) AS gs,
                sum(s_1.sek_1::double precision * vs.anteil) AS sek_1,
                sum(s_1.sek_2::double precision * vs.anteil) AS sek_2,
                sum(s_1.foerderschu::double precision * vs.anteil) AS
                  foerderschu,
                sum(s_1.sek12::double precision * vs.anteil) AS sek12,
                sum(s_1.bbs_vz::double precision * vs.anteil) AS bbs_vz,
                sum(s_1.bbs_tz::double precision * vs.anteil) AS bbs_tz,
                sum(s_1.berufsschueler::double precision * vs.anteil) AS bs
         FROM einrichtungen.schueler s_1,
              _einrichtungen._vz_schulen vs
         WHERE s_1.id = vs.id
         GROUP BY vs.id_zone
       ) s ON v.id = s.vz_id
       LEFT JOIN 
       (
         SELECT vh.id_zone AS vz_id,
                sum(h_1.studierende::double precision * vh.anteil) AS
                  studierende
         FROM einrichtungen.hochschulen h_1,
              _einrichtungen._vz_hochschulen vh
         WHERE h_1.id = vh.id
         GROUP BY vh.id_zone
       ) h ON v.id = h.vz_id
       LEFT JOIN 
       (
         SELECT vk.id_zone AS vz_id,
                sum(k_1.betreuungsplaetze::double precision * vk.anteil) AS
                  betreuungsplaetze
         FROM einrichtungen.kitas k_1,
              _einrichtungen._vz_kitas vk
         WHERE k_1.id = vk.id
         GROUP BY vk.id_zone
       ) k ON v.id = k.vz_id;		   
	   
CREATE OR REPLACE VIEW strukturdaten.vz_erledigung(
    vz_id,
    postfilialen,
    bankfilialen,
    aerzte,
    pflegeheime,
    klinikbetten,
    verwaltung,
    apotheken)
AS
  SELECT v.id AS vz_id,
         COALESCE(p.postfilialen, 0::bigint) AS postfilialen,
         COALESCE(b.bankfilialen, 0::bigint) AS bankfilialen,
         COALESCE(a.aerzte, 0::bigint) AS aerzte,
         COALESCE(pf.pflegeheime, 0::bigint) AS pflegeheime,
         COALESCE(kl.klinikbetten::bigint, 0::bigint) AS klinikbetten,
         COALESCE(bu.verwaltung, 0::bigint) + COALESCE(la.verwaltung, 0::bigint)
           + COALESCE(k.verwaltung, 0::bigint) AS verwaltung,
         COALESCE(ap.apotheken, 0::bigint) AS apotheken
  FROM verkehrszellen.view_vz_aktuell v
       LEFT JOIN 
       (
         SELECT pv.id_zone AS vz_id,
                count(*) AS apotheken
         FROM einrichtungen.apotheken p_1,
              _einrichtungen._vz_apotheken pv
         WHERE p_1.id = pv.id
         GROUP BY pv.id_zone
       ) ap ON v.id = ap.vz_id
       LEFT JOIN 
       (
         SELECT pv.id_zone AS vz_id,
                count(*) AS postfilialen
         FROM einrichtungen.postfilialen p_1,
              _einrichtungen._vz_postfilialen pv
         WHERE p_1.id = pv.id
         GROUP BY pv.id_zone
       ) p ON v.id = p.vz_id
       LEFT JOIN 
       (
         SELECT bv.id_zone AS vz_id,
                count(*) AS bankfilialen
         FROM einrichtungen.bankfilialen b1,
              _einrichtungen._vz_bankfilialen bv
         WHERE b1.id = bv.id
         GROUP BY bv.id_zone
       ) b ON v.id = b.vz_id
       LEFT JOIN 
       (
         SELECT av.id_zone AS vz_id,
                count(*) AS aerzte
         FROM einrichtungen.aerzte a1,
              _einrichtungen._vz_aerzte av
         WHERE a1.id = av.id
         GROUP BY av.id_zone
       ) a ON v.id = a.vz_id
       LEFT JOIN 
       (
         SELECT av.id_zone AS vz_id,
                count(*) AS pflegeheime
         FROM einrichtungen.pflegeheime a1,
              _einrichtungen._vz_pflegeheime av
         WHERE a1.id = av.id
         GROUP BY av.id_zone
       ) pf ON v.id = pf.vz_id
       LEFT JOIN 
       (
         SELECT av.id_zone AS vz_id,
                sum(a1.besch_2015 / 5::double precision)::integer AS
                  klinikbetten
         FROM einrichtungen.kliniken a1,
              _einrichtungen._vz_kliniken av
         WHERE a1.id = av.id
         GROUP BY av.id_zone
       ) kl ON v.id = kl.vz_id
       LEFT JOIN 
       (
         SELECT av.id_zone AS vz_id,
                sum(a1.besucherverkehr) AS verwaltung
         FROM apl.besch_kommune_2015 a1,
              _apl._vz_besch_kommune_2015 av
         WHERE a1.id = av.id
         GROUP BY av.id_zone
       ) k ON v.id = k.vz_id
       LEFT JOIN 
       (
         SELECT av.id_zone AS vz_id,
                sum(a1.besucherverkehr) AS verwaltung
         FROM apl.besch_oe_land_2015 a1,
              _apl._vz_besch_oe_land_2015 av
         WHERE a1.id = av.id
         GROUP BY av.id_zone
       ) la ON v.id = la.vz_id
       LEFT JOIN 
       (
         SELECT av.id_zone AS vz_id,
                sum(a1.besucherverkehr) AS verwaltung
         FROM apl.besch_oe_bund_2015 a1,
              _apl._vz_besch_oe_bund_2015 av
         WHERE a1.id = av.id
         GROUP BY av.id_zone
       ) bu ON v.id = bu.vz_id;
	   
CREATE OR REPLACE VIEW strukturdaten.vz_ew_alkl(
    vz_id,
    alkl_id,
    alkl,
    einw)
AS
  SELECT v.id AS vz_id,
         a.alkl_id,
         a.alkl,
         CASE
           WHEN y.jahr = 2015 THEN COALESCE(e2015.einw, 0::double precision)
           ELSE COALESCE(ep.einw, 0::double precision)
         END AS einw
  FROM meta.current_year y,
       verkehrszellen.view_vz_aktuell v
       CROSS JOIN einwohner.altersklassen a
       LEFT JOIN einwohner.view_l_m_vz_ew_alkl_2015 e2015 ON v.id = e2015.vz_id
         AND a.alkl_id = e2015.alkl_id
       LEFT JOIN einwohner.view_l4_vz_ew_alkl_prognosejahr ep ON v.id = ep.vz_id
         AND a.alkl_id = ep.alkl_id;
		 
CREATE OR REPLACE VIEW strukturdaten.vz_ew_alkl_crosstab(
    vz_id,
    "X00_05",
    "X06_10",
    "X11_14",
    "X15_18",
    "X19_22",
    "X23_30",
    "X31_35",
    "X36_40",
    "X41_45",
    "X46_50",
    "X51_55",
    "X56_60",
    "X61_65",
    "X66_70",
    "X71_75",
    "X76_80",
    "X81___",
    "Summe",
    geom,
    objectid)
AS
  SELECT v.id AS vz_id,
         COALESCE(crosstab."X00_05", 0::real) AS "X00_05",
         COALESCE(crosstab."X06_10", 0::real) AS "X06_10",
         COALESCE(crosstab."X11_14", 0::real) AS "X11_14",
         COALESCE(crosstab."X15_18", 0::real) AS "X15_18",
         COALESCE(crosstab."X19_22", 0::real) AS "X19_22",
         COALESCE(crosstab."X23_30", 0::real) AS "X23_30",
         COALESCE(crosstab."X31_35", 0::real) AS "X31_35",
         COALESCE(crosstab."X36_40", 0::real) AS "X36_40",
         COALESCE(crosstab."X41_45", 0::real) AS "X41_45",
         COALESCE(crosstab."X46_50", 0::real) AS "X46_50",
         COALESCE(crosstab."X51_55", 0::real) AS "X51_55",
         COALESCE(crosstab."X56_60", 0::real) AS "X56_60",
         COALESCE(crosstab."X61_65", 0::real) AS "X61_65",
         COALESCE(crosstab."X66_70", 0::real) AS "X66_70",
         COALESCE(crosstab."X71_75", 0::real) AS "X71_75",
         COALESCE(crosstab."X76_80", 0::real) AS "X76_80",
         COALESCE(crosstab."X81___", 0::real) AS "X81___",
         COALESCE(es.einw, 0::double precision) AS "Summe",
         v.geom,
         row_number() OVER(
  ORDER BY v.id)::integer AS objectid
  FROM verkehrszellen.view_vz_aktuell v
       LEFT JOIN crosstab('
    SELECT e.vz_id AS rowid, a.alkl as attribute, e.einw as value
    FROM
            einwohner.altersklassen AS a,
                strukturdaten.vz_ew_alkl AS e
    WHERE a.alkl_id = e.alkl_id
    ORDER BY e.vz_id, a.alkl'::text, '
        select distinct ON (alkl_id) alkl
        FROM strukturdaten.vz_ew_alkl
        ORDER BY alkl_id'::text) crosstab(vz_id integer, "X00_05" real, "X06_10"
          real, "X11_14" real, "X15_18" real, "X19_22" real, "X23_30" real,
          "X31_35" real, "X36_40" real, "X41_45" real, "X46_50" real, "X51_55"
          real, "X56_60" real, "X61_65" real, "X66_70" real, "X71_75" real,
          "X76_80" real, "X81___" real) ON v.id = crosstab.vz_id
       LEFT JOIN 
       (
         SELECT e.vz_id,
                sum(e.einw) AS einw
         FROM strukturdaten.vz_ew_alkl e
         GROUP BY e.vz_id
       ) es ON es.vz_id = crosstab.vz_id
  ORDER BY v.id;
  
 CREATE OR REPLACE VIEW strukturdaten.vz_freizeit(
    vz_id,
    gastronomie,
    fitness,
    baeder,
    kinos,
    sportstaetten,
    buehnen,
    erholungsflaechen)
AS
  SELECT v.id AS vz_id,
         COALESCE(g1.gastronomie, 0::bigint) + COALESCE(g2.gastronomie, 0::
           bigint) + COALESCE(g3.gastronomie, 0::bigint) AS gastronomie,
         COALESCE(f.fitness, 0::bigint) AS fitness,
         COALESCE(b.baeder, 0::bigint) AS baeder,
         COALESCE(k.kinos, 0::bigint) AS kinos,
         COALESCE(s.sportstaetten, 0::bigint) AS sportstaetten,
         COALESCE(bu.buehnen, 0::bigint) AS buehnen,
         COALESCE(e.erholungsflaechen, 0::double precision) AS erholungsflaechen
  FROM verkehrszellen.view_vz_aktuell v
       LEFT JOIN 
       (
         SELECT pv.id_zone AS vz_id,
                count(*) AS gastronomie
         FROM einrichtungen.gastronomiebetriebe p_1,
              _einrichtungen._vz_gastronomiebetriebe pv
         WHERE p_1.id = pv.id
         GROUP BY pv.id_zone
       ) g1 ON v.id = g1.vz_id
       LEFT JOIN 
       (
         SELECT pv.id_zone AS vz_id,
                count(*) AS gastronomie
         FROM einrichtungen.gastronomie2 p_1,
              _einrichtungen._vz_gastronomie2 pv
         WHERE p_1.id = pv.id
         GROUP BY pv.id_zone
       ) g2 ON v.id = g2.vz_id
       LEFT JOIN 
       (
         SELECT pv.id_zone AS vz_id,
                count(*) AS gastronomie
         FROM einrichtungen.gastro_hotel_osm p_1,
              _einrichtungen._vz_gastro_hotel_osm pv
         WHERE p_1.id = pv.id
         GROUP BY pv.id_zone
       ) g3 ON v.id = g3.vz_id
       LEFT JOIN 
       (
         SELECT bv.id_zone AS vz_id,
                count(*) AS fitness
         FROM einrichtungen.fitness b1,
              _einrichtungen._vz_fitness bv
         WHERE b1.id = bv.id
         GROUP BY bv.id_zone
       ) f ON v.id = f.vz_id
       LEFT JOIN 
       (
         SELECT av.id_zone AS vz_id,
                count(*) AS baeder
         FROM einrichtungen.baeder a1,
              _einrichtungen._vz_baeder av
         WHERE a1.id = av.id
         GROUP BY av.id_zone
       ) b ON v.id = b.vz_id
       LEFT JOIN 
       (
         SELECT av.id_zone AS vz_id,
                sum(a1.plaetze) AS kinos
         FROM (
                SELECT a1_1.id,
                       CASE a1_1.kategorie
                         WHEN 1 THEN 50
                         WHEN 2 THEN 200
                         WHEN 3 THEN 500
                         ELSE NULL::integer
                       END AS plaetze
                FROM einrichtungen.kinos a1_1
              ) a1,
              _einrichtungen._vz_kinos av
         WHERE a1.id = av.id
         GROUP BY av.id_zone
       ) k ON v.id = k.vz_id
       LEFT JOIN 
       (
         SELECT av.id_zone AS vz_id,
                count(*) AS sportstaetten
         FROM einrichtungen.sport a1,
              _einrichtungen._vz_sport av
         WHERE a1.id = av.id
         GROUP BY av.id_zone
       ) s ON v.id = s.vz_id
       LEFT JOIN 
       (
         SELECT av.id_zone AS vz_id,
                sum(a1.plaetze) AS buehnen
         FROM (
                SELECT a1_1.id,
                       CASE a1_1.kategorie
                         WHEN 1 THEN 20
                         WHEN 2 THEN 100
                         WHEN 3 THEN 500
                         ELSE NULL::integer
                       END AS plaetze
                FROM einrichtungen.buehnen a1_1
              ) a1,
              _einrichtungen._vz_buehnen av
         WHERE a1.id = av.id
         GROUP BY av.id_zone
       ) bu ON v.id = bu.vz_id
       LEFT JOIN 
       (
         SELECT av.id AS vz_id,
                sum(a1.factor * av.weight) / 10000::double precision AS
                  erholungsflaechen
         FROM landuse.matview_erholungsflaeche a1,
              _landuse._vz_matview_erholungsflaeche av
         WHERE a1.gid = av.gid
         GROUP BY av.id
       ) e ON v.id = e.vz_id;
	   
CREATE OR REPLACE VIEW strukturdaten.vz_apl_prognosejahr_crosstab(
    vz_id,
    ap_a,
    ap_bf,
    ap_gi,
    ap_jn,
    ap_ou,
    geom,
    objectid)
AS
  SELECT vr.vz_id,
         vr.ap_a,
         vr.ap_bf,
         vr.ap_gi,
         vr.ap_jn,
         vr.ap_ou,
         vr.geom,
         row_number() OVER(
  ORDER BY vr.vz_id)::integer AS objectid
  FROM (
         SELECT v.id AS vz_id,
                COALESCE(crosstab."A", 0::real) AS ap_a,
                COALESCE(crosstab."BF", 0::real) AS ap_bf,
                COALESCE(crosstab."GI", 0::real) AS ap_gi,
                COALESCE(crosstab."JN", 0::real) AS ap_jn,
                COALESCE(crosstab."OU", 0::real) AS ap_ou,
                v.geom
         FROM verkehrszellen.view_vz_aktuell v
              LEFT JOIN crosstab('
    SELECT a.vz_id AS rowid, a.wz_bereich as attribute, a.besch as value
    FROM
        strukturdaten.vz_apl_prognosejahr AS a'::text, '
        select distinct ON (wz_bereich) wz_bereich
        FROM classifications.wirtschaftsabschnitt_aufschlaege_auf_svb
        ORDER BY wz_bereich'::text) crosstab(vz_id integer, "A" real, "BF" real,
          "GI" real, "JN" real, "OU" real) ON v.id = crosstab.vz_id
       ) vr;
	   
CREATE OR REPLACE VIEW strukturdaten.vz_ew_alkl_2015_crosstab(
    vz_id,
    "X00_05",
    "X06_10",
    "X11_14",
    "X15_18",
    "X19_22",
    "X23_30",
    "X31_35",
    "X36_40",
    "X41_45",
    "X46_50",
    "X51_55",
    "X56_60",
    "X61_65",
    "X66_70",
    "X71_75",
    "X76_80",
    "X81___",
    "Summe",
    geom,
    objectid)
AS
  SELECT v.id AS vz_id,
         COALESCE(crosstab."X00_05", 0::real) AS "X00_05",
         COALESCE(crosstab."X06_10", 0::real) AS "X06_10",
         COALESCE(crosstab."X11_14", 0::real) AS "X11_14",
         COALESCE(crosstab."X15_18", 0::real) AS "X15_18",
         COALESCE(crosstab."X19_22", 0::real) AS "X19_22",
         COALESCE(crosstab."X23_30", 0::real) AS "X23_30",
         COALESCE(crosstab."X31_35", 0::real) AS "X31_35",
         COALESCE(crosstab."X36_40", 0::real) AS "X36_40",
         COALESCE(crosstab."X41_45", 0::real) AS "X41_45",
         COALESCE(crosstab."X46_50", 0::real) AS "X46_50",
         COALESCE(crosstab."X51_55", 0::real) AS "X51_55",
         COALESCE(crosstab."X56_60", 0::real) AS "X56_60",
         COALESCE(crosstab."X61_65", 0::real) AS "X61_65",
         COALESCE(crosstab."X66_70", 0::real) AS "X66_70",
         COALESCE(crosstab."X71_75", 0::real) AS "X71_75",
         COALESCE(crosstab."X76_80", 0::real) AS "X76_80",
         COALESCE(crosstab."X81___", 0::real) AS "X81___",
         COALESCE(es.einw, 0::double precision) AS "Summe",
         v.geom,
         row_number() OVER(
  ORDER BY v.id)::integer AS objectid
  FROM verkehrszellen.view_vz_aktuell v
       LEFT JOIN crosstab('
    SELECT e.vz_id AS rowid, a.alkl as attribute, e.einw as value
    FROM
        einwohner.altersklassen AS a,
            einwohner.view_l_m_vz_ew_alkl_2015 AS e
    WHERE a.alkl_id = e.alkl_id
    ORDER BY e.vz_id, a.alkl'::text, '
        select distinct ON (alkl_id) alkl
        FROM einwohner.view_l_m_vz_ew_alkl_2015
        ORDER BY alkl_id'::text) crosstab(vz_id integer, "X00_05" real, "X06_10"
          real, "X11_14" real, "X15_18" real, "X19_22" real, "X23_30" real,
          "X31_35" real, "X36_40" real, "X41_45" real, "X46_50" real, "X51_55"
          real, "X56_60" real, "X61_65" real, "X66_70" real, "X71_75" real,
          "X76_80" real, "X81___" real) ON v.id = crosstab.vz_id
       LEFT JOIN 
       (
         SELECT e.vz_id,
                sum(e.einw) AS einw
         FROM einwohner.view_l_m_vz_ew_alkl_2015 e
         GROUP BY e.vz_id
       ) es ON es.vz_id = crosstab.vz_id
  ORDER BY v.id;
  
  
  CREATE OR REPLACE VIEW
  strukturdaten.vz_ew_alkl_prognosejahr_crosstab_2015_mit_progdaten(
    vz_id,
    "X00_05",
    "X06_10",
    "X11_14",
    "X15_18",
    "X19_22",
    "X23_30",
    "X31_35",
    "X36_40",
    "X41_45",
    "X46_50",
    "X51_55",
    "X56_60",
    "X61_65",
    "X66_70",
    "X71_75",
    "X76_80",
    "X81___",
    "Summe",
    geom,
    objectid)
AS
  SELECT v.id AS vz_id,
         COALESCE(crosstab."X00_05", 0::real) AS "X00_05",
         COALESCE(crosstab."X06_10", 0::real) AS "X06_10",
         COALESCE(crosstab."X11_14", 0::real) AS "X11_14",
         COALESCE(crosstab."X15_18", 0::real) AS "X15_18",
         COALESCE(crosstab."X19_22", 0::real) AS "X19_22",
         COALESCE(crosstab."X23_30", 0::real) AS "X23_30",
         COALESCE(crosstab."X31_35", 0::real) AS "X31_35",
         COALESCE(crosstab."X36_40", 0::real) AS "X36_40",
         COALESCE(crosstab."X41_45", 0::real) AS "X41_45",
         COALESCE(crosstab."X46_50", 0::real) AS "X46_50",
         COALESCE(crosstab."X51_55", 0::real) AS "X51_55",
         COALESCE(crosstab."X56_60", 0::real) AS "X56_60",
         COALESCE(crosstab."X61_65", 0::real) AS "X61_65",
         COALESCE(crosstab."X66_70", 0::real) AS "X66_70",
         COALESCE(crosstab."X71_75", 0::real) AS "X71_75",
         COALESCE(crosstab."X76_80", 0::real) AS "X76_80",
         COALESCE(crosstab."X81___", 0::real) AS "X81___",
         COALESCE(es.einw, 0::double precision) AS "Summe",
         v.geom,
         row_number() OVER(
  ORDER BY v.id)::integer AS objectid
  FROM verkehrszellen.view_vz_aktuell v
       LEFT JOIN crosstab('
    SELECT e.vz_id AS rowid, a.alkl as attribute, e.einw as value
    FROM
            einwohner.altersklassen AS a,
                einwohner.view_l4_vz_ew_alkl_prognosejahr AS e
    WHERE a.alkl_id = e.alkl_id
    ORDER BY e.vz_id, a.alkl'::text, '
        select distinct ON (alkl_id) alkl
        FROM einwohner.view_l4_vz_ew_alkl_prognosejahr
        ORDER BY alkl_id'::text) crosstab(vz_id integer, "X00_05" real, "X06_10"
          real, "X11_14" real, "X15_18" real, "X19_22" real, "X23_30" real,
          "X31_35" real, "X36_40" real, "X41_45" real, "X46_50" real, "X51_55"
          real, "X56_60" real, "X61_65" real, "X66_70" real, "X71_75" real,
          "X76_80" real, "X81___" real) ON v.id = crosstab.vz_id
       LEFT JOIN 
       (
         SELECT e.vz_id,
                sum(e.einw) AS einw
         FROM einwohner.view_l4_vz_ew_alkl_prognosejahr e
         GROUP BY e.vz_id
       ) es ON es.vz_id = crosstab.vz_id
  ORDER BY v.id;
  
  CREATE OR REPLACE VIEW strukturdaten.vz_personengruppen(
    vz_id,
    pgr,
    einw)
AS
  SELECT v.id AS vz_id,
         p.id AS pgr,
         CASE
           WHEN y.jahr = 2015 THEN COALESCE(p2015.einw, 0::double precision)
           ELSE COALESCE(pp.einw, 0::double precision)
         END AS einw
  FROM meta.current_year y,
       verkehrszellen.view_vz_aktuell v
       CROSS JOIN strukturdaten.pgr_name p
       LEFT JOIN einwohner.vz_personengruppen_2015 p2015 ON v.id = p2015.vz_id
         AND p.id = p2015.pgr
       LEFT JOIN einwohner.vz_personengruppen_prognosejahr pp ON v.id = pp.vz_id
         AND p.id = pp.pgr;
		 
CREATE OR REPLACE VIEW strukturdaten.vz_pgr_regionsring(
    vz_id,
    "Gsch",
    "Sch18",
    "Sch2",
    "AzuBi",
    "EmP",
    "EoP",
    "NEmP",
    "NEoP",
    "R75mP",
    "R75oP",
    "R99mP",
    "R99oP")
AS
  SELECT v.id AS vz_id,
         COALESCE(r."Gsch", 0::double precision) AS "Gsch",
         COALESCE(r."Sch18", 0::double precision) AS "Sch18",
         COALESCE(r."Sch2", 0::double precision) AS "Sch2",
         COALESCE(r."AzuBi", 0::double precision) AS "AzuBi",
         COALESCE(r."EmP", 0::double precision) AS "EmP",
         COALESCE(r."EoP", 0::double precision) AS "EoP",
         COALESCE(r."NEmP", 0::double precision) AS "NEmP",
         COALESCE(r."NEoP", 0::double precision) AS "NEoP",
         COALESCE(r."R75mP", 0::double precision) AS "R75mP",
         COALESCE(r."R75oP", 0::double precision) AS "R75oP",
         COALESCE(r."R99mP", 0::double precision) AS "R99mP",
         COALESCE(r."R99oP", 0::double precision) AS "R99oP"
  FROM verkehrszellen.view_vz_aktuell v
       LEFT JOIN einwohner.regionsring_einwohner r ON v.id = r.vz_nr;
	   
CREATE OR REPLACE VIEW strukturdaten.vz_apl_wz_bereiche(
    vz_id,
    ap,
    ap_dl,
    ap_a,
    ap_bf,
    ap_gi,
    ap_jn,
    ap_ou)
AS
  SELECT a.vz_id,
         (a.ap_a + a.ap_bf + a.ap_gi + a.ap_jn + a.ap_ou)::double precision AS
           ap,
         (a.ap_gi + a.ap_jn + a.ap_ou)::double precision AS ap_dl,
         a.ap_a::double precision AS ap_a,
         a.ap_bf::double precision AS ap_bf,
         a.ap_gi::double precision AS ap_gi,
         a.ap_jn::double precision AS ap_jn,
         a.ap_ou::double precision AS ap_ou
  FROM strukturdaten.vz_apl_prognosejahr_crosstab a,
       verkehrszellen.mview_vz_progbez p
  WHERE a.vz_id = p.vz_id AND
        p.progbez_id >(- 1)
  UNION ALL
  SELECT v.id AS vz_id,
         r.ap,
         r.ap_dl,
         r.ap_a,
         r.ap_bf,
         r.ap_gi,
         r.ap_jn,
         r.ap_ou
  FROM verkehrszellen.view_vz_aktuell v,
       strukturdaten.struktur_regionsring_2015 r
  WHERE v.id = r.vz_id;
  
CREATE OR REPLACE VIEW strukturdaten.vz_handel(
    vz_id,
    eh_perid,
    eh_aperid,
    vkfl_periodisch,
    vkfl_aperiodisch)
AS
  SELECT v.id AS vz_id,
         COALESCE(s.zp_per, 0::double precision) AS eh_perid,
         COALESCE(s.zp_aper, 0::double precision) AS eh_aperid,
         COALESCE(s.vfl_perid, 0::double precision) AS vkfl_periodisch,
         COALESCE(s.vfl_aperid, 0::double precision) AS vkfl_aperiodisch
  FROM verkehrszellen.view_vz_aktuell v
       LEFT JOIN 
       (
         SELECT vh.id_zone AS vz_id,
                sum(h.zielp_periodisch * vh.anteil) AS zp_per,
                sum(h.zielp_aperidoisch * vh.anteil) AS zp_aper,
                sum(h.vkf * s_1.periodisch) AS vfl_perid,
                sum(h.vkf * s_1.aperiodisch) AS vfl_aperid
         FROM handel.einzelhandel h,
              _handel._vz_einzelhandel vh,
              handel.eh_sortiment_zp_besch s_1,
              meta.current_year y
         WHERE h.id = vh.id AND
               h.branche = s_1.id_sortiment AND
               h.valid_from <= y.jahr AND
               h.valid_to >= y.jahr
         GROUP BY vh.id_zone
       ) s ON v.id = s.vz_id,
       verkehrszellen.mview_vz_progbez p
  WHERE v.id = p.vz_id AND
        p.progbez_id >(- 1)
  UNION ALL
  SELECT v.id AS vz_id,
         r.eh_per AS eh_perid,
         r.eh_aper AS eh_aperid,
         r.eh_per AS vkfl_periodisch,
         r.eh_aper AS vkfl_aperiodisch
  FROM verkehrszellen.view_vz_aktuell v,
       strukturdaten.struktur_regionsring_2015 r
  WHERE v.id = r.vz_id;
  
 CREATE OR REPLACE VIEW strukturdaten.vz_zielpotenziel_aktivitaeten(
    vz_id,
    arbpl,
    grundsch,
    schpl_18,
    berufs,
    schulplaetze2,
    vkf_period,
    vkf_aperiod,
    privgel,
    einwohner)
AS
  SELECT z.vz_id,
         z.ap AS arbpl,
         z.gs AS grundsch,
         z.sek12 AS schpl_18,
         z.bs AS berufs,
         z.studierende AS schulplaetze2,
         z.eh_period * z.faktor_eink AS vkf_period,
         z.eh_aperiod * z.faktor_eink AS vkf_aperiod,
         (0.2::double precision * z.ew6 + z.ap_dl + z.eh_period + z.eh_aperiod)
           * z.faktor_eink AS privgel,
         z.ew AS einwohner
  FROM (
         SELECT v.id AS vz_id,
                COALESCE(e."Summe" - e."X00_05", 0::double precision) AS ew6,
                COALESCE(a.ap, 0::double precision) AS ap,
                COALESCE(a.ap_dl, 0::double precision) AS ap_dl,
                COALESCE(b.gs, 0::double precision) AS gs,
                COALESCE(b.sek12, 0::double precision) AS sek12,
                COALESCE(b.bs, 0::double precision) AS bs,
                COALESCE(b.studierende, 0::double precision) AS studierende,
                COALESCE(gt.faktor_eink, 0::double precision) AS faktor_eink,
                COALESCE(h.eh_perid, 0::double precision) AS eh_period,
                COALESCE(h.eh_aperid, 0::double precision) AS eh_aperiod,
                COALESCE(e."Summe", 0::double precision) AS ew
         FROM verkehrszellen.view_vz_aktuell v
              LEFT JOIN strukturdaten.vz_ew_alkl_crosstab e ON v.id = e.vz_id
              LEFT JOIN strukturdaten.vz_apl_wz_bereiche a ON v.id = a.vz_id
              LEFT JOIN strukturdaten.vz_bildung b ON v.id = b.vz_id
              LEFT JOIN strukturdaten.vz_handel h ON v.id = h.vz_id
              LEFT JOIN verkehrszellen.matview_vz_aktuell_gebietstypen gt ON
                v.id = gt.id,
              verkehrszellen.mview_vz_progbez p
         WHERE v.id = p.vz_id AND
               p.progbez_id >(- 1)
         UNION ALL
         SELECT v.id AS vz_id,
                r.ew::real AS ew6,
                r.ap::real AS ap,
                r.ap_dl::real AS ap_dl,
                0::double precision AS gs,
                0::double precision AS sek12,
                0::double precision AS bs,
                r.studpl AS studierende,
                1::double precision AS faktor_eink,
                r.eh_per AS eh_period,
                r.eh_aper AS eh_aperiod,
                r.ew
         FROM verkehrszellen.view_vz_aktuell v,
              strukturdaten.struktur_regionsring_2015 r
         WHERE v.id = r.vz_id
       ) z;
	   
CREATE OR REPLACE VIEW strukturdaten.results(
    vz_id,
    zone_name,
    geom,
    "X00_05",
    "X06_10",
    "X11_14",
    "X15_18",
    "X19_22",
    "X23_30",
    "X31_35",
    "X36_40",
    "X41_45",
    "X46_50",
    "X51_55",
    "X56_60",
    "X61_65",
    "X66_70",
    "X71_75",
    "X76_80",
    "X81___",
    "Summe",
    "Gsch",
    "Sch18",
    "Sch2",
    "AzuBi",
    "EmP",
    "EoP",
    "NEmP",
    "NEoP",
    "R75mP",
    "R75oP",
    "R99mP",
    "R99oP",
    faktor_eh,
    gs,
    sek_1,
    sek_2,
    foerderschueler,
    sek12,
    bs,
    bbs_vz,
    bbs_tz,
    studierende,
    zielp_periodisch,
    zielp_aperiodisch,
    vkfl_periodisch,
    vkfl_aperiodisch,
    ew6,
    ap,
    ap_dl,
    ap_a,
    ap_bf,
    ap_gi,
    ap_jn,
    ap_ou,
    "Arbpl",
    "Grundsch",
    "Schpl_18",
    "Berufs",
    "Schulplaetze2",
    "Vkf_period",
    "Vkf_aperiod",
    "PrivGel",
    "Einwohner",
    kita_plaetze,
    postfilialen,
    bankfilialen,
    aerzte,
    pflegeheime,
    klinikbetten,
    gastronomie,
    fitness,
    baeder,
    kinos,
    sportstaetten,
    buehnen,
    erholungsflaechen,
    verwaltung,
    apotheken)
AS
  SELECT v.id AS vz_id,
         v.zone_name,
         v.geom,
         e."X00_05",
         e."X06_10",
         e."X11_14",
         e."X15_18",
         e."X19_22",
         e."X23_30",
         e."X31_35",
         e."X36_40",
         e."X41_45",
         e."X46_50",
         e."X51_55",
         e."X56_60",
         e."X61_65",
         e."X66_70",
         e."X71_75",
         e."X76_80",
         e."X81___",
         e."Summe",
         p."Gsch",
         p."Sch18",
         p."Sch2",
         p."AzuBi",
         p."EmP",
         p."EoP",
         p."NEmP",
         p."NEoP",
         p."R75mP",
         p."R75oP",
         p."R99mP",
         p."R99oP",
         gt.faktor_eink AS faktor_eh,
         b.gs,
         b.sek_1,
         b.sek_2,
         b.foerderschueler,
         b.sek12,
         b.bs,
         b.bbs_vz,
         b.bbs_tz,
         b.studierende,
         h.eh_perid AS zielp_periodisch,
         h.eh_aperid AS zielp_aperiodisch,
         h.vkfl_periodisch,
         h.vkfl_aperiodisch,
         e."Summe" - e."X00_05" AS ew6,
         a.ap,
         a.ap_dl,
         a.ap_a,
         a.ap_bf,
         a.ap_gi,
         a.ap_jn,
         a.ap_ou,
         z.arbpl AS "Arbpl",
         z.grundsch AS "Grundsch",
         z.schpl_18 AS "Schpl_18",
         z.berufs AS "Berufs",
         z.schulplaetze2 AS "Schulplaetze2",
         z.vkf_period AS "Vkf_period",
         z.vkf_aperiod AS "Vkf_aperiod",
         z.privgel AS "PrivGel",
         z.einwohner AS "Einwohner",
         b.betreuungsplaetze AS kita_plaetze,
         er.postfilialen,
         er.bankfilialen,
         er.aerzte,
         er.pflegeheime,
         er.klinikbetten,
         fr.gastronomie,
         fr.fitness,
         fr.baeder,
         fr.kinos,
         fr.sportstaetten,
         fr.buehnen,
         fr.erholungsflaechen,
         er.verwaltung,
         er.apotheken
  FROM verkehrszellen.view_vz_aktuell v
       LEFT JOIN strukturdaten.vz_ew_alkl_crosstab e ON v.id = e.vz_id
       LEFT JOIN strukturdaten.vz_pgr_crosstab p ON v.id = p.vz_id
       LEFT JOIN strukturdaten.vz_apl_wz_bereiche a ON v.id = a.vz_id
       LEFT JOIN strukturdaten.vz_bildung b ON v.id = b.vz_id
       LEFT JOIN strukturdaten.vz_handel h ON v.id = h.vz_id
       LEFT JOIN verkehrszellen.matview_vz_aktuell_gebietstypen gt ON v.id =
         gt.id
       LEFT JOIN strukturdaten.vz_zielpotenziel_aktivitaeten z ON v.id = z.vz_id
       LEFT JOIN strukturdaten.vz_erledigung er ON v.id = er.vz_id
       LEFT JOIN strukturdaten.vz_freizeit fr ON v.id = fr.vz_id
  ORDER BY v.id;
  
CREATE OR REPLACE VIEW strukturdaten.results_gebietstypen(
    vz_id,
    zone_name,
    geom,
    "X00_05",
    "X06_10",
    "X11_14",
    "X15_18",
    "X19_22",
    "X23_30",
    "X31_35",
    "X36_40",
    "X41_45",
    "X46_50",
    "X51_55",
    "X56_60",
    "X61_65",
    "X66_70",
    "X71_75",
    "X76_80",
    "X81___",
    "Summe",
    "Gsch",
    "Sch18",
    "Sch2",
    "AzuBi",
    "EmP",
    "EoP",
    "NEmP",
    "NEoP",
    "R75mP",
    "R75oP",
    "R99mP",
    "R99oP",
    faktor_eh,
    gs,
    sek_1,
    sek_2,
    foerderschueler,
    sek12,
    bs,
    bbs_vz,
    bbs_tz,
    studierende,
    zielp_periodisch,
    zielp_aperiodisch,
    vkfl_periodisch,
    vkfl_aperiodisch,
    ew6,
    ap,
    ap_dl,
    ap_a,
    ap_bf,
    ap_gi,
    ap_jn,
    ap_ou,
    "Arbpl",
    "Grundsch",
    "Schpl_18",
    "Berufs",
    "Schulplaetze2",
    "Vkf_period",
    "Vkf_aperiod",
    "PrivGel",
    "Einwohner",
    kita_plaetze,
    postfilialen,
    bankfilialen,
    aerzte,
    pflegeheime,
    klinikbetten,
    gastronomie,
    fitness,
    baeder,
    kinos,
    sportstaetten,
    buehnen,
    erholungsflaechen,
    verwaltung,
    apotheken)
AS
  SELECT z.typ12 AS vz_id,
         z.typ12::text AS zone_name,
         z.geom,
         sum(r."X00_05") AS "X00_05",
         sum(r."X06_10") AS "X06_10",
         sum(r."X11_14") AS "X11_14",
         sum(r."X15_18") AS "X15_18",
         sum(r."X19_22") AS "X19_22",
         sum(r."X23_30") AS "X23_30",
         sum(r."X31_35") AS "X31_35",
         sum(r."X36_40") AS "X36_40",
         sum(r."X41_45") AS "X41_45",
         sum(r."X46_50") AS "X46_50",
         sum(r."X51_55") AS "X51_55",
         sum(r."X56_60") AS "X56_60",
         sum(r."X61_65") AS "X61_65",
         sum(r."X66_70") AS "X66_70",
         sum(r."X71_75") AS "X71_75",
         sum(r."X76_80") AS "X76_80",
         sum(r."X81___") AS "X81___",
         sum(r."Summe") AS "Summe",
         sum(r."Gsch") AS "Gsch",
         sum(r."Sch18") AS "Sch18",
         sum(r."Sch2") AS "Sch2",
         sum(r."AzuBi") AS "AzuBi",
         sum(r."EmP") AS "EmP",
         sum(r."EoP") AS "EoP",
         sum(r."NEmP") AS "NEmP",
         sum(r."NEoP") AS "NEoP",
         sum(r."R75mP") AS "R75mP",
         sum(r."R75oP") AS "R75oP",
         sum(r."R99mP") AS "R99mP",
         sum(r."R99oP") AS "R99oP",
         sum(r.faktor_eh) AS faktor_eh,
         sum(r.gs) AS gs,
         sum(r.sek_1) AS sek_1,
         sum(r.sek_2) AS sek_2,
         sum(r.foerderschueler) AS foerderschueler,
         sum(r.sek12) AS sek12,
         sum(r.bs) AS bs,
         sum(r.bbs_vz) AS bbs_vz,
         sum(r.bbs_tz) AS bbs_tz,
         sum(r.studierende) AS studierende,
         sum(r.zielp_periodisch) AS zielp_periodisch,
         sum(r.zielp_aperiodisch) AS zielp_aperiodisch,
         sum(r.vkfl_periodisch) AS vkfl_periodisch,
         sum(r.vkfl_aperiodisch) AS vkfl_aperiodisch,
         sum(r.ew6) AS ew6,
         sum(r.ap) AS ap,
         sum(r.ap_dl) AS ap_dl,
         sum(r.ap_a) AS ap_a,
         sum(r.ap_bf) AS ap_bf,
         sum(r.ap_gi) AS ap_gi,
         sum(r.ap_jn) AS ap_jn,
         sum(r.ap_ou) AS ap_ou,
         sum(r."Arbpl") AS "Arbpl",
         sum(r."Grundsch") AS "Grundsch",
         sum(r."Schpl_18") AS "Schpl_18",
         sum(r."Berufs") AS "Berufs",
         sum(r."Schulplaetze2") AS "Schulplaetze2",
         sum(r."Vkf_period") AS "Vkf_period",
         sum(r."Vkf_aperiod") AS "Vkf_aperiod",
         sum(r."PrivGel") AS "PrivGel",
         sum(r."Einwohner") AS "Einwohner",
         sum(r.kita_plaetze) AS kita_plaetze,
         sum(r.postfilialen) AS postfilialen,
         sum(r.bankfilialen) AS bankfilialen,
         sum(r.aerzte) AS aerzte,
         sum(r.pflegeheime) AS pflegeheime,
         sum(r.klinikbetten) AS klinikbetten,
         sum(r.gastronomie) AS gastronomie,
         sum(r.fitness) AS fitness,
         sum(r.baeder) AS baeder,
         sum(r.kinos) AS kinos,
         sum(r.sportstaetten) AS sportstaetten,
         sum(r.buehnen) AS buehnen,
         sum(r.erholungsflaechen) AS erholungsflaechen,
         sum(r.verwaltung) AS verwaltung,
         sum(r.apotheken) AS apotheken
  FROM strukturdaten.results r,
       verkehrszellen.matview_vz_aktuell_gebietstypen gt,
       verkehrszellen.schiene_zentralitaet z
  WHERE r.vz_id = gt.id AND
        gt.typeno = z.typeno AND
        gt.anschiene = z.an_schiene
  GROUP BY z.typ12,
           z.geom;
		   
CREATE OR REPLACE VIEW strukturdaten.results_prognosebezirke(
    vz_id,
    zone_name,
    geom,
    gkz,
    "X00_05",
    "X06_10",
    "X11_14",
    "X15_18",
    "X19_22",
    "X23_30",
    "X31_35",
    "X36_40",
    "X41_45",
    "X46_50",
    "X51_55",
    "X56_60",
    "X61_65",
    "X66_70",
    "X71_75",
    "X76_80",
    "X81___",
    "Summe",
    "Gsch",
    "Sch18",
    "Sch2",
    "AzuBi",
    "EmP",
    "EoP",
    "NEmP",
    "NEoP",
    "R75mP",
    "R75oP",
    "R99mP",
    "R99oP",
    faktor_eh,
    gs,
    sek_1,
    sek_2,
    foerderschueler,
    sek12,
    bs,
    bbs_vz,
    bbs_tz,
    studierende,
    zielp_periodisch,
    zielp_aperiodisch,
    vkfl_periodisch,
    vkfl_aperiodisch,
    ew6,
    ap,
    ap_dl,
    ap_a,
    ap_bf,
    ap_gi,
    ap_jn,
    ap_ou,
    "Arbpl",
    "Grundsch",
    "Schpl_18",
    "Berufs",
    "Schulplaetze2",
    "Vkf_period",
    "Vkf_aperiod",
    "PrivGel",
    "Einwohner",
    kita_plaetze,
    postfilialen,
    bankfilialen,
    aerzte,
    pflegeheime,
    klinikbetten,
    gastronomie,
    fitness,
    baeder,
    kinos,
    sportstaetten,
    buehnen,
    erholungsflaechen,
    verwaltung,
    apotheken)
AS
  SELECT p.id AS vz_id,
         p.name2 AS zone_name,
         p.geom,
         p.gkz,
         sum(r."X00_05") AS "X00_05",
         sum(r."X06_10") AS "X06_10",
         sum(r."X11_14") AS "X11_14",
         sum(r."X15_18") AS "X15_18",
         sum(r."X19_22") AS "X19_22",
         sum(r."X23_30") AS "X23_30",
         sum(r."X31_35") AS "X31_35",
         sum(r."X36_40") AS "X36_40",
         sum(r."X41_45") AS "X41_45",
         sum(r."X46_50") AS "X46_50",
         sum(r."X51_55") AS "X51_55",
         sum(r."X56_60") AS "X56_60",
         sum(r."X61_65") AS "X61_65",
         sum(r."X66_70") AS "X66_70",
         sum(r."X71_75") AS "X71_75",
         sum(r."X76_80") AS "X76_80",
         sum(r."X81___") AS "X81___",
         sum(r."Summe") AS "Summe",
         sum(r."Gsch") AS "Gsch",
         sum(r."Sch18") AS "Sch18",
         sum(r."Sch2") AS "Sch2",
         sum(r."AzuBi") AS "AzuBi",
         sum(r."EmP") AS "EmP",
         sum(r."EoP") AS "EoP",
         sum(r."NEmP") AS "NEmP",
         sum(r."NEoP") AS "NEoP",
         sum(r."R75mP") AS "R75mP",
         sum(r."R75oP") AS "R75oP",
         sum(r."R99mP") AS "R99mP",
         sum(r."R99oP") AS "R99oP",
         sum(r.faktor_eh) AS faktor_eh,
         sum(r.gs) AS gs,
         sum(r.sek_1) AS sek_1,
         sum(r.sek_2) AS sek_2,
         sum(r.foerderschueler) AS foerderschueler,
         sum(r.sek12) AS sek12,
         sum(r.bs) AS bs,
         sum(r.bbs_vz) AS bbs_vz,
         sum(r.bbs_tz) AS bbs_tz,
         sum(r.studierende) AS studierende,
         sum(r.zielp_periodisch) AS zielp_periodisch,
         sum(r.zielp_aperiodisch) AS zielp_aperiodisch,
         sum(r.vkfl_periodisch) AS vkfl_periodisch,
         sum(r.vkfl_aperiodisch) AS vkfl_aperiodisch,
         sum(r.ew6) AS ew6,
         sum(r.ap) AS ap,
         sum(r.ap_dl) AS ap_dl,
         sum(r.ap_a) AS ap_a,
         sum(r.ap_bf) AS ap_bf,
         sum(r.ap_gi) AS ap_gi,
         sum(r.ap_jn) AS ap_jn,
         sum(r.ap_ou) AS ap_ou,
         sum(r."Arbpl") AS "Arbpl",
         sum(r."Grundsch") AS "Grundsch",
         sum(r."Schpl_18") AS "Schpl_18",
         sum(r."Berufs") AS "Berufs",
         sum(r."Schulplaetze2") AS "Schulplaetze2",
         sum(r."Vkf_period") AS "Vkf_period",
         sum(r."Vkf_aperiod") AS "Vkf_aperiod",
         sum(r."PrivGel") AS "PrivGel",
         sum(r."Einwohner") AS "Einwohner",
         sum(r.kita_plaetze) AS kita_plaetze,
         sum(r.postfilialen) AS postfilialen,
         sum(r.bankfilialen) AS bankfilialen,
         sum(r.aerzte) AS aerzte,
         sum(r.pflegeheime) AS pflegeheime,
         sum(r.klinikbetten) AS klinikbetten,
         sum(r.gastronomie) AS gastronomie,
         sum(r.fitness) AS fitness,
         sum(r.baeder) AS baeder,
         sum(r.kinos) AS kinos,
         sum(r.sportstaetten) AS sportstaetten,
         sum(r.buehnen) AS buehnen,
         sum(r.erholungsflaechen) AS erholungsflaechen,
         sum(r.verwaltung) AS verwaltung,
         sum(r.apotheken) AS apotheken
  FROM strukturdaten.results r,
       verkehrszellen.mview_vz_progbez vp,
       raumeinheiten.prognosebezirke p
  WHERE r.vz_id = vp.vz_id AND
        p.id = vp.progbez_id
  GROUP BY p.id,
           p.name2,
           p.geom,
           p.gkz;
		   
CREATE OR REPLACE VIEW strukturdaten.results_gemeinden(
    vz_id,
    zone_name,
    geom,
    "X00_05",
    "X06_10",
    "X11_14",
    "X15_18",
    "X19_22",
    "X23_30",
    "X31_35",
    "X36_40",
    "X41_45",
    "X46_50",
    "X51_55",
    "X56_60",
    "X61_65",
    "X66_70",
    "X71_75",
    "X76_80",
    "X81___",
    "Summe",
    "Gsch",
    "Sch18",
    "Sch2",
    "AzuBi",
    "EmP",
    "EoP",
    "NEmP",
    "NEoP",
    "R75mP",
    "R75oP",
    "R99mP",
    "R99oP",
    faktor_eh,
    gs,
    sek_1,
    sek_2,
    foerderschueler,
    sek12,
    bs,
    bbs_vz,
    bbs_tz,
    studierende,
    zielp_periodisch,
    zielp_aperiodisch,
    vkfl_periodisch,
    vkfl_aperiodisch,
    ew6,
    ap,
    ap_dl,
    ap_a,
    ap_bf,
    ap_gi,
    ap_jn,
    ap_ou,
    "Arbpl",
    "Grundsch",
    "Schpl_18",
    "Berufs",
    "Schulplaetze2",
    "Vkf_period",
    "Vkf_aperiod",
    "PrivGel",
    "Einwohner",
    kita_plaetze,
    postfilialen,
    bankfilialen,
    aerzte,
    pflegeheime,
    klinikbetten,
    gastronomie,
    fitness,
    baeder,
    kinos,
    sportstaetten,
    buehnen,
    erholungsflaechen,
    verwaltung,
    apotheken)
AS
  SELECT g.gkz6 AS vz_id,
         g.name::text AS zone_name,
         g.geom,
         sum(r."X00_05") AS "X00_05",
         sum(r."X06_10") AS "X06_10",
         sum(r."X11_14") AS "X11_14",
         sum(r."X15_18") AS "X15_18",
         sum(r."X19_22") AS "X19_22",
         sum(r."X23_30") AS "X23_30",
         sum(r."X31_35") AS "X31_35",
         sum(r."X36_40") AS "X36_40",
         sum(r."X41_45") AS "X41_45",
         sum(r."X46_50") AS "X46_50",
         sum(r."X51_55") AS "X51_55",
         sum(r."X56_60") AS "X56_60",
         sum(r."X61_65") AS "X61_65",
         sum(r."X66_70") AS "X66_70",
         sum(r."X71_75") AS "X71_75",
         sum(r."X76_80") AS "X76_80",
         sum(r."X81___") AS "X81___",
         sum(r."Summe") AS "Summe",
         sum(r."Gsch") AS "Gsch",
         sum(r."Sch18") AS "Sch18",
         sum(r."Sch2") AS "Sch2",
         sum(r."AzuBi") AS "AzuBi",
         sum(r."EmP") AS "EmP",
         sum(r."EoP") AS "EoP",
         sum(r."NEmP") AS "NEmP",
         sum(r."NEoP") AS "NEoP",
         sum(r."R75mP") AS "R75mP",
         sum(r."R75oP") AS "R75oP",
         sum(r."R99mP") AS "R99mP",
         sum(r."R99oP") AS "R99oP",
         sum(r.faktor_eh) AS faktor_eh,
         sum(r.gs) AS gs,
         sum(r.sek_1) AS sek_1,
         sum(r.sek_2) AS sek_2,
         sum(r.foerderschueler) AS foerderschueler,
         sum(r.sek12) AS sek12,
         sum(r.bs) AS bs,
         sum(r.bbs_vz) AS bbs_vz,
         sum(r.bbs_tz) AS bbs_tz,
         sum(r.studierende) AS studierende,
         sum(r.zielp_periodisch) AS zielp_periodisch,
         sum(r.zielp_aperiodisch) AS zielp_aperiodisch,
         sum(r.vkfl_periodisch) AS vkfl_periodisch,
         sum(r.vkfl_aperiodisch) AS vkfl_aperiodisch,
         sum(r.ew6) AS ew6,
         sum(r.ap) AS ap,
         sum(r.ap_dl) AS ap_dl,
         sum(r.ap_a) AS ap_a,
         sum(r.ap_bf) AS ap_bf,
         sum(r.ap_gi) AS ap_gi,
         sum(r.ap_jn) AS ap_jn,
         sum(r.ap_ou) AS ap_ou,
         sum(r."Arbpl") AS "Arbpl",
         sum(r."Grundsch") AS "Grundsch",
         sum(r."Schpl_18") AS "Schpl_18",
         sum(r."Berufs") AS "Berufs",
         sum(r."Schulplaetze2") AS "Schulplaetze2",
         sum(r."Vkf_period") AS "Vkf_period",
         sum(r."Vkf_aperiod") AS "Vkf_aperiod",
         sum(r."PrivGel") AS "PrivGel",
         sum(r."Einwohner") AS "Einwohner",
         sum(r.kita_plaetze) AS kita_plaetze,
         sum(r.postfilialen) AS postfilialen,
         sum(r.bankfilialen) AS bankfilialen,
         sum(r.aerzte) AS aerzte,
         sum(r.pflegeheime) AS pflegeheime,
         sum(r.klinikbetten) AS klinikbetten,
         sum(r.gastronomie) AS gastronomie,
         sum(r.fitness) AS fitness,
         sum(r.baeder) AS baeder,
         sum(r.kinos) AS kinos,
         sum(r.sportstaetten) AS sportstaetten,
         sum(r.buehnen) AS buehnen,
         sum(r.erholungsflaechen) AS erholungsflaechen,
         sum(r.verwaltung) AS verwaltung,
         sum(r.apotheken) AS apotheken
  FROM strukturdaten.results_prognosebezirke r,
       raumeinheiten.gemeinden_region g
  WHERE r.gkz = g.gkz6
  GROUP BY g.gkz6,
           g.name,
           g.geom;
		   
		   