-- færdigbehandlet i perioden
DECLARE @year char(4) = '@år'
DECLARE @month char(2) = '@måned'


SELECT
	(SELECT COUNT(DISTINCT sagID) FROM BBRsagsstyring.dbo.vSagerFærdigbehandletTilladelse
	 WHERE
		BehandletTidspunkt >= CONVERT(datetime, @year + @month + '01')
		AND BehandletTidspunkt <= EOMONTH(CONVERT(datetime, @year + @month + '01'))
	) 'Tilladelsessager'
	,
	(SELECT COUNT(DISTINCT sag001Byggesagsnummer) FROM LOIS.DAF_BBR.BBRSag bbrSag
	 WHERE
		bbrSag.status IN (9, 11, 12, 13, 14)
		AND CONVERT(date,bbrSag.virkningFra) >= CONVERT(date, @year + '-' + @month + '-01')
		AND CONVERT(date,bbrSag.virkningFra) <= CONVERT(date, EOMONTH(CONVERT(datetime, @year + '-' + @month + '-01')))
	) 'Afslutningssager'