DELETE FROM service_template WHERE name IN ('Boot From Fiber Channel SAN', 'Boot from iSCSI SAN', 'Deploy VMware Cluster with Netapp Storage', 'Deploy VMware Cluster with FCoE Storage') AND template_locked = 'true';