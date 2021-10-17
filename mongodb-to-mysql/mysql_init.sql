CREATE TABLE vaccinations (
    `_id` varchar(24) primary key not null,
    `channel` varchar(10),
    `createdAt` datetime,
    `updatedAt` datetime,
    `vaccination_type` varchar(10) ,
    `vaccination_vaccineCode` varchar(50),
    `vaccination_vaccineDate` date,
    `vaccination_vaccineLocation_faskesCode` varchar(50) ,
    `vaccination_vaccineLocation_name` varchar(100),
    `vaccination_vaccineStatus` int,
    `vaccinePatient_bornDate` date,
    `vaccinePatient_fullName` varchar(255) ,
    `vaccinePatient_gender` varchar(2),
    `vaccinePatient_mobileNumber` varchar(20),
    `vaccinePatient_nik` varchar(16),
    `vaccinePatient_profession` varchar(20),
    `_ingestion_ts` datetime
);
