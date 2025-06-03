SELECT
	  (SELECT COUNT(DISTINCT sag001Byggesagsnummer) FROM DAF_BBR.BBRSag bbrB INNER JOIN BBRsagsstyring.dbo.vSagerIkkeTildeltTilladelse sitt ON bbrB.sag001Byggesagsnummer = sitt.sagsnummer WHERE bbrB.[status] NOT IN (9, 11, 12, 13, 14))
	+ (SELECT COUNT(DISTINCT sag001Byggesagsnummer) FROM DAF_BBR.BBRSag bbrB INNER JOIN BBRsagsstyring.dbo.vSagerIkkeTildeltTilladelse sitt ON bbrB.sag001Byggesagsnummer = sitt.structuraSagsnummer WHERE bbrB.[status] NOT IN (9, 11, 12, 13, 14))
	+ (SELECT COUNT(DISTINCT sag001Byggesagsnummer) FROM DAF_BBR.BBRSag bbrB INNER JOIN BBRsagsstyring.dbo.vSagerTildeltTilladelse stt ON bbrB.sag001Byggesagsnummer = stt.sagsnummer WHERE bbrB.[status] NOT IN (9, 11, 12, 13, 14))
	+ (SELECT COUNT(DISTINCT sag001Byggesagsnummer) FROM DAF_BBR.BBRSag bbrB INNER JOIN BBRsagsstyring.dbo.vSagerTildeltTilladelse stt ON bbrB.sag001Byggesagsnummer = stt.structuraSagsnummer WHERE bbrB.[status] NOT IN (9, 11, 12, 13, 14))
	AS 'Tilladelsessager'

	,
	
	  (SELECT COUNT(DISTINCT sag001Byggesagsnummer) FROM DAF_BBR.BBRSag bbrB INNER JOIN BBRsagsstyring.dbo.vSagerIkkeTildeltAfsluttet sita ON bbrB.sag001Byggesagsnummer = sita.sagsnummer WHERE bbrB.[status] NOT IN (9, 11, 12, 13, 14))
	+ (SELECT COUNT(DISTINCT sag001Byggesagsnummer) FROM DAF_BBR.BBRSag bbrB INNER JOIN BBRsagsstyring.dbo.vSagerIkkeTildeltAfsluttet sita ON bbrB.sag001Byggesagsnummer = sita.structuraSagsnummer WHERE	bbrB.[status] NOT IN (9, 11, 12, 13, 14))
	+ (SELECT COUNT(DISTINCT sag001Byggesagsnummer) FROM DAF_BBR.BBRSag bbrB INNER JOIN BBRsagsstyring.dbo.vSagerTildeltAfsluttet sita ON bbrB.sag001Byggesagsnummer = sita.sagsnummer WHERE bbrB.[status] NOT IN (9, 11, 12, 13, 14))
	+ (SELECT COUNT(DISTINCT sag001Byggesagsnummer) FROM DAF_BBR.BBRSag bbrB INNER JOIN BBRsagsstyring.dbo.vSagerTildeltAfsluttet sita ON bbrB.sag001Byggesagsnummer = sita.structuraSagsnummer WHERE bbrB.[status] NOT IN (9, 11, 12, 13, 14))
	AS 'Afslutningssager'
