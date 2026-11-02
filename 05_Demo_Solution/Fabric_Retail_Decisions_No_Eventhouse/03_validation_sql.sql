-- Run against the Lakehouse SQL analytics endpoint (read-only).
SELECT YEAR(s.SalesDate) AS SalesYear, SUM(s.Revenue) AS ElectronicsRevenue
FROM fact_daily_sales s JOIN dim_product p ON s.ProductId=p.ProductId
WHERE p.Category='Electronics' AND MONTH(s.SalesDate)=9 AND YEAR(s.SalesDate) IN (2025,2026)
GROUP BY YEAR(s.SalesDate) ORDER BY SalesYear;

SELECT s.StoreId, YEAR(s.SalesDate) AS SalesYear, SUM(s.Revenue) AS Revenue
FROM fact_daily_sales s JOIN dim_product p ON s.ProductId=p.ProductId
WHERE p.Category='Electronics' AND MONTH(s.SalesDate)=9
GROUP BY s.StoreId,YEAR(s.SalesDate) ORDER BY s.StoreId,SalesYear;

SELECT StoreId, IsLowStock, OnHand FROM fact_inventory WHERE IsLowStock=1;
SELECT COUNT(*) AS NewEvidenceCount FROM new_evidence;
SELECT * FROM new_evidence ORDER BY EvidenceId;
