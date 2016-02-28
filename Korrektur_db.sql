ALTER TABLE raumeinheiten.stat_bez DROP COLUMN IF EXISTS gkz6;
ALTER TABLE raumeinheiten.stat_bez ADD COLUMN gkz6 INTEGER;

UPDATE raumeinheiten.stat_bez b
SET gkz6 = g.gkz6::integer
FROM raumeinheiten.gemeinden g
WHERE b.gem_nummer = g.ob_id;

CREATE OR REPLACE VIEW einwohner.view_b1_all_buildings(
    building_id,
    gestyp,
    sb_nummer,
    gem_nummer,
    summe,
    geom)
AS
  SELECT g.fid AS building_id,
         g.gestyp,
         b.sb_nummer,
         b.gkz6,
         g.summe,
         g.point AS geom
  FROM einwohner.geb_umland_einwohner_2008 g,
       _einwohner._statbez_geb_umland_einwohner_2008 gb,
       raumeinheiten.stat_bez b
  WHERE g.fid = gb.fid AND
        b.sb_nummer = gb.sb_nummer
  UNION ALL
  SELECT n.gid + 1000000 AS building_id,
         n.gestyp,
         b.sb_nummer,
         b.gem_nummer,
         0 AS summe,
         n.point AS geom
  FROM einwohner.newbuildings2015 n,
       _einwohner._statbez_newbuildings2015 nb,
       raumeinheiten.stat_bez b
  WHERE n.gid = nb.gid AND
        b.sb_nummer = nb.sb_nummer;
        
REFRESH MATERIALIZED VIEW einwohner.view_b1_m_all_buildings;

CREATE OR REPLACE VIEW einwohner.view_d1_building_imp_ew_alkl(
    building_id,
    gestyp,
    vz_nr__,
    gem_nummer,
    sb_nummer,
    alkl_id,
    ew)
AS
  SELECT g.building_id,
         g.gestyp,
         0::double precision AS vz_nr__,
         g.gem_nummer,
         s.gkz6 AS gem_nummer,
         c.alkl_id,
         c.ew_je_geb AS ew
  FROM einwohner.view_c1_mittl_einw_alkl_je_gebtyp c,
       einwohner.view_b1_m_all_buildings g,
       raumeinheiten.stat_bez s
  WHERE c.sb_nummer = g.sb_nummer AND
        c.gestyp = g.gestyp AND
        g.sb_nummer = s.sb_nummer AND
        g.summe = 0 AND
        g.gestyp <> 3 AND
        s.gem_nummer > 201000
  UNION ALL
  SELECT g0.fid AS building_id,
         g0.gestyp,
         g0.vz_nr__,
         g0.gem_nummer,
         g0.sb_nummer,
         g0.alkl_id,
         g0.ew
  FROM einwohner.geb_umland_einwohner_long_2008 g0,
       _einwohner._statbez_geb_umland_einwohner_2008 gs,
       raumeinheiten.stat_bez s
  WHERE g0.fid = gs.fid AND
        gs.sb_nummer = s.sb_nummer AND
        s.gem_nummer > 201000;

CREATE OR REPLACE VIEW einwohner.view_j_ew2015_alkl_geb_umland(
    building_id,
    vz_nr__,
    gem_nummer,
    sb_nummer,
    alkl_id,
    ew,
    ew_hw)
AS
  SELECT g.building_id,
         0::double precision AS vz_nr__,
         s.gkz6 AS gem_nummer,
         s.sb_nummer,
         g.alkl_id,
         g.ew_hw * i2.kf_hw +(g.ew - g.ew_hw) * i2.kf_nw AS ew,
         g.ew_hw * i2.kf_hw AS ew_hw
  FROM einwohner.view_i2_kf2015_alkl_umland i2,
       einwohner.view_i03_m_building_ewsynth_alkl_nach_abgleich_mit_statbez g,
       raumeinheiten.stat_bez s
  WHERE g.sb_nummer = s.sb_nummer AND
        i2.gkz = s.gkz6 AND
        i2.alkl_id = g.alkl_id;

REFRESH MATERIALIZED VIEW einwohner.view_g_m_buildings_ewsynth_alkl;
REFRESH MATERIALIZED VIEW einwohner.view_i03_m_building_ewsynth_alkl_nach_abgleich_mit_statbez;
REFRESH MATERIALIZED VIEW einwohner.view_j_m_ew2015_alkl_geb_umland;
REFRESH MATERIALIZED VIEW einwohner.view_l_m_vz_ew_alkl_2015;

DELETE FROM verkehrszellen.zentralitaet
WHERE rn > 100;
INSERT INTO verkehrszellen.zentralitaet (rn, typeno, geom)
SELECT row_number() OVER(ORDER BY typeno, (d).path)::integer + 1000 AS rn, typeno, (d).geom
FROM (
SELECT z.typeno + 10 AS typeno, st_dump(st_intersection(z.geom, u.geom)) AS d
FROM verkehrszellen.zentralitaet z,
(
SELECT st_union(geom) AS geom
FROM verkehrszellen.vzvep g
WHERE g.nr > 50000) u
) a
WHERE st_npoints((d).geom)>3
AND st_isvalid((d).geom);

INSERT INTO verkehrszellen.zentralitaet (rn, typeno, geom)
SELECT row_number() OVER(ORDER BY typeno, (d).path)::integer + 2000 AS rn, typeno, (d).geom
FROM(
SELECT z.typeno, st_dump(st_intersection(z.geom, u.geom)) AS d
FROM verkehrszellen.zentralitaet z,
(
SELECT st_union(geom) AS geom
FROM verkehrszellen.vzvep g
WHERE g.nr < 50000) u
WHERE z.rn <= 100) a
WHERE st_npoints((d).geom)>3
AND st_isvalid((d).geom);

DELETE FROM verkehrszellen.zentralitaet
WHERE rn < 100;

ANALYZE verkehrszellen.zentralitaet;

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

REFRESH MATERIALIZED VIEW verkehrszellen.matview_vz_aktuell_gebietstypen;

INSERT INTO meta.queries (id, command, message, weight)
VALUES(0, 'REFRESH MATERIALIZED VIEW verkehrszellen.matview_vzaktuell_centroids;', 'Centroide der Verkehrszellen berechnet', 1);