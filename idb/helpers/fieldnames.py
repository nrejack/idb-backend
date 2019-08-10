from __future__ import division, absolute_import, print_function
import json
import string
from collections import defaultdict

'''
The namespaces are ...
'''

namespaces = {
    "http://rs.tdwg.org/dwc/terms/": "dwc",
    "http://purl.org/dc/terms/": "dcterms",
    "http://purl.org/dc/elements/1.1/": "dc",
    "http://rs.tdwg.org/ac/terms/": "ac",
    "http://ns.adobe.com/xap/1.0/rights/": "xmpRights",
    "http://ns.adobe.com/xap/1.0/": "xmp",
    "http://iptc.org/std/Iptc4xmpExt/1.0/xmlns/": "Iptc4xmpExt",
    "http://iptc.org/std/Iptc4xmpExt/2008-02-29/": "Iptc4xmpExt",
    "http://portal.idigbio.org/terms/": "idigbio",
    "http://symbiota.org/terms/": "symbiota",
    "http://portal.idigbio.org/terms/inhs/": "inhs",
    "http://www.w3.org/2003/01/geo/wgs84_pos#": "wgs84_pos",
    "http://rs.gbif.org/terms/1.0/": "gbif",
    "http://iucn.org/terms/": "iucn",
    "http://portal.idigbio.org/terms/fcc/": "fcc",
    "http://ns.adobe.com/photoshop/1.0/": "photoshop",
    "http://ns.adobe.com/exif/1.0/": "exif",
    "http://purl.org/NET/aec/NET/aec/": "aec",
    "http://purl.org/NET/aec/": "aec",
    "http://zooarchnet.org/dwc/terms/": "zan"
}

namespaces_rev = {v:k for k, v in namespaces.items()}

# Temp hack to make sure aec is right
namespaces_rev["aec"] = "http://purl.org/NET/aec/"

# Manual Reverse Override
namespaces_rev["Iptc4xmpExt"] = "http://iptc.org/std/Iptc4xmpExt/2008-02-29/"

'''
types map the namespace URI to a Compact URI / CURIE
'''
types = {
    "http://purl.org/NET/aec/associatedTaxa": {"shortname": "aec:associatedTaxa"},
    "http://rs.gbif.org/terms/1.0/Identifier": {"shortname": "gbif:Identifier"},
    "http://rs.gbif.org/terms/1.0/Image":  { "shortname": "dwc:Multimedia"},
    "http://rs.gbif.org/terms/1.0/Multimedia": { "shortname": "dwc:Multimedia"},
    "http://rs.gbif.org/terms/1.0/Reference": {"shortname": "gbif:Reference"},
    "http://rs.gbif.org/terms/1.0/SpeciesProfile": { "shortname": "gbif:SpeciesProfile" },
    "http://rs.gbif.org/terms/1.0/VernacularName": { "shortname": "gbif:VernacularName" },
    "http://rs.tdwg.org/ac/terms/Audubon_Core": { "shortname": "dwc:Multimedia"},
    "http://rs.tdwg.org/ac/terms/multimedia": { "shortname": "dwc:Multimedia"},
    "http://rs.tdwg.org/ac/terms/Multimedia": { "shortname": "dwc:Multimedia"},
    "http://rs.tdwg.org/dwc/terms/Identification": { "shortname": "dwc:Identification" },
    "http://rs.tdwg.org/dwc/terms/MeasurementOrFact": {"shortname": "dwc:MeasurementOrFact"},
    "http://rs.tdwg.org/dwc/terms/occurrence": { "shortname": "dwc:Occurrence" },
    "http://rs.tdwg.org/dwc/terms/Occurrence": { "shortname": "dwc:Occurrence" },
    "http://rs.tdwg.org/dwc/terms/ResourceRelationship": { "shortname": "dwc:ResourceRelationship" },
    "http://rs.tdwg.org/dwc/terms/Taxon": {"shortname": "dwc:Taxon"},
    "http://zooarchnet.org/dwc/terms/ChronometricDate": {"shortname": "zan:ChronometricDate"},
    "http://zooarchnet.org/dwc/terms/ChronometricAge": {"shortname": "zan:ChronometricAge"}
}

'''
The translate_dict is used to...
'''
translate_dict = {
    "ac:accessURI": ["ac:accessURI", "dwc:Multimedia"],
    "ac:associatedObservationReference": ["ac:associatedObservationReference", "dwc:Multimedia"],
    "ac:associatedSpecimenReference": ["ac:associatedSpecimenReference", "dwc:Multimedia"],
    "ac:attributionLinkURL": ["ac:attributionLinkURL", "dwc:Multimedia"],
    "ac:attributionLogoURL": ["ac:attributionLogoURL", "dwc:Multimedia"],
    "ac:bestQualityAccessURI": ["ac:bestQualityAccessURI", "dwc:Multimedia"],
    "ac:bestQualityExtent": ["ac:bestQualityExtent", "dwc:Multimedia"],
    "ac:bestQualityFormat": ["ac:bestQualityFormat", "dwc:Multimedia"],
    "ac:bestQualityVariantDescription": ["ac:bestQualityVariantDescription", "dwc:Multimedia"],
    "ac:caption": ["ac:caption", "dwc:Multimedia"],
    "ac:captureDevice": ["ac:captureDevice", "dwc:Multimedia"],
    "ac:commenter": ["ac:commenter", "dwc:Multimedia"],
    "ac:commenterLiteral": ["ac:commenterLiteral", "dwc:Multimedia"],
    "ac:comments": ["ac:comments", "dwc:Multimedia"],
    "ac:derivedFrom": ["ac:derivedFrom", "dwc:Multimedia"],
    "ac:digitizationDate": ["ac:digitizationDate", "dwc:Multimedia"],
    "ac:fundingAttribution": ["ac:fundingAttribution", "dwc:Multimedia"],
    "ac:furtherInformationURL": ["ac:furtherInformationURL", "dwc:Multimedia"],
    "ac:hashFunction": ["ac:hashFunction", "dwc:Multimedia"],
    "ac:hashValue": ["ac:hashValue", "dwc:Multimedia"],
    "ac:hasServiceAccessPoint": ["ac:hasServiceAccessPoint", "dwc:Multimedia"],
    "ac:IDofContainingCollection": ["ac:IDofContainingCollection", "dwc:Multimedia"],
    "ac:licenseLogoURL": ["ac:licenseLogoURL", "dwc:Multimedia"],
    "ac:licensingException": ["ac:licensingException", "dwc:Multimedia"],
    "ac:metadataCreator": ["ac:metadataCreator", "dwc:Multimedia"],
    "ac:metadataCreatorLiteral": ["ac:metadataCreatorLiteral", "dwc:Multimedia"],
    "ac:metadataLanguage": ["ac:metadataLanguage", "dwc:Multimedia"],
    "ac:metadataLanguageLiteral": ["ac:metadataLanguageLiteral", "dwc:Multimedia"],
    "ac:metadataProvider": ["ac:metadataProvider", "dwc:Multimedia"],
    "ac:metadataProviderLiteral": ["ac:metadataProviderLiteral", "dwc:Multimedia"],
    "ac:otherScientificName": ["ac:otherScientificName", "dwc:Multimedia"],
    "ac:physicalSetting": ["ac:physicalSetting", "dwc:Multimedia"],
    "ac:provider": ["ac:provider", "dwc:Multimedia"],
    "ac:providerID": ["ac:providerID", "dwc:Multimedia"],
    "ac:providerLiteral": ["ac:providerLiteral", "dwc:Multimedia"],
    "ac:providerManagedID": ["ac:providerManagedID", "dwc:Multimedia"],
    "ac:relatedResourceID": ["ac:relatedResourceID", "dwc:Multimedia"],
    "ac:resourceCreationTechnique": ["ac:resourceCreationTechnique", "dwc:Multimedia"],
    "ac:reviewer": ["ac:reviewer", "dwc:Multimedia"],
    "ac:reviewerComments": ["ac:reviewerComments", "dwc:Multimedia"],
    "ac:reviewerLiteral": ["ac:reviewerLiteral", "dwc:Multimedia"],
    "ac:serviceExpectation": ["ac:serviceExpectation", "dwc:Multimedia"],
    "ac:subjectCategoryVocabulary": ["ac:subjectCategoryVocabulary", "dwc:Multimedia"],
    "ac:subjectOrientation": ["ac:subjectOrientation", "dwc:Multimedia"],
    "ac:subjectPart": ["ac:subjectPart", "dwc:Multimedia"],
    "ac:subtype": ["ac:subtype", "dwc:Multimedia"],
    "ac:subtypeLiteral": ["ac:subtypeLiteral", "dwc:Multimedia"],
    "ac:tag": ["ac:tag", "dwc:Multimedia"],
    "ac:taxonCount": ["ac:taxonCount", "dwc:Multimedia"],
    "ac:taxonCoverage": ["ac:taxonCoverage", "dwc:Multimedia"],
    "ac:thumbnailAccessURI": ["ac:thumbnailAccessURI", "dwc:Multimedia"],
    "ac:thumbnailFormat": ["ac:thumbnailFormat", "dwc:Multimedia"],
    "ac:timeOfDay": ["ac:timeOfDay", "dwc:Multimedia"],
    "ac:variant": ["ac:variant", "dwc:Multimedia"],
    "ac:variantDescription": ["ac:variantDescription", "dwc:Multimedia"],
    "ac:variantLiteral": ["ac:variantLiteral", "dwc:Multimedia"],
    "ac:goodQualityAccessURI": ["ac:goodQualityAccessURI", "dwc:Multimedia"],
    "aec:associatedAuthor": ["aec:associatedAuthor", "aec:associatedTaxa"],
    "aec:associatedCollectionLocation": ["aec:associatedCollectionLocation", "aec:associatedTaxa"],
    "aec:associatedCommonName": ["aec:associatedCommonName", "aec:associatedTaxa"],
    "aec:associatedCondition": ["aec:associatedCondition", "aec:associatedTaxa"],
    "aec:associatedDeterminedBy": ["aec:associatedDeterminedBy", "aec:associatedTaxa"],
    "aec:associatedEmergenceVerbatimDate": ["aec:associatedEmergenceVerbatimDate", "aec:associatedTaxa"],
    "aec:associatedFamily": ["aec:associatedFamily", "aec:associatedTaxa"],
    "aec:associatedGenus": ["aec:associatedGenus", "aec:associatedTaxa"],
    "aec:associatedLocationOnHost": ["aec:associatedLocationOnHost", "aec:associatedTaxa"],
    "aec:associatedNotes": ["aec:associatedNotes", "aec:associatedTaxa"],
    "aec:associatedOccuranceID": ["aec:associatedOccuranceID", "aec:associatedTaxa"],
    "aec:associatedRelationshipTerm": ["aec:associatedRelationshipTerm", "aec:associatedTaxa"],
    "aec:associatedRelationshipURI": ["aec:associatedRelationshipURI", "aec:associatedTaxa"],
    "aec:associatedScientificName": ["aec:associatedScientificName", "aec:associatedTaxa"],
    "aec:associatedSpecificEpithet": ["aec:associatedSpecificEpithet", "aec:associatedTaxa"],
    "aec:isCultivar": ["aec:isCultivar", "aec:associatedTaxa"],
    "Annotations": [None, "dwc:Multimedia"],
    "associate_author": ["idigbio:associateAuthor", "dwc:Occurrence"],
    "associate_commonName": ["idigbio:associateCommonName", "dwc:Occurrence"],
    "associate_condition": ["idigbio:associateCondition", "dwc:Occurrence"],
    "associate_determinedBy": ["idigbio:associateDeterminedBy", "dwc:Occurrence"],
    "associate_identifier": ["idigbio:associateIdentifier", "dwc:Occurrence"],
    "associate_location": ["idigbio:associateLocation", "dwc:Occurrence"],
    "associate_notes": ["idigbio:associateNotes", "dwc:Occurrence"],
    "associate_relationship": ["idigbio:associateRelationship", "dwc:Occurrence"],
    "associatedFamily": ["idigbio:associatedFamily", "dwc:Occurrence"],
    "BasisOfRecord": ["dwc:basisOfRecord", "dwc:Occurrence"],
    "basisOfRecord": ["dwc:basisOfRecord", "dwc:Occurrence"],
    "batchID": [None, "dwc:Multimedia"],
    "bed": ["dwc:bed", "dwc:Occurrence"],
    "catalogNumber": ["dwc:catalogNumber", "dwc:Occurrence"],
    "class": ["dwc:class", "dwc:Occurrence"],
    "Collection": ["dwc:collectionCode", "dwc:Occurrence"],
    "collectionCode": ["dwc:collectionCode", "dwc:Occurrence"],
    "collector": ["dwc:recordedBy", "dwc:Occurrence"],
    "Collector": ["dwc:recordedBy", "dwc:Occurrence"],
    "CoordinateUncertaintyinMeters": ["dwc:coordinateUncertaintyinMeters", "dwc:Occurrence"],
    "coreid": ["coreid", "dwc:Text:Extension"],
    "country": ["dwc:country", "dwc:Occurrence"],
    "Country": ["dwc:country", "dwc:Occurrence"],
    "county": ["dwc:county", "dwc:Occurrence"],
    "County": ["dwc:county", "dwc:Occurrence"],
    "CSVfilePath": [None, "dwc:Multimedia"],
    "row number": [None, "dwc:Occurrence"],
    "day": ["dwc:day", "dwc:Occurrence"],
    "DayCollected": ["dwc:day", "dwc:Occurrence"],
    "dc:creator": ["dc:creator", "dcterms"],
    "dc:format": ["dc:format", "dcterms"],
    "dc:language": ["dc:language", "dcterms"],
    "dc:rights": ["dc:rights", "dcterms"],
    "dc:source": ["dc:source", "dcterms"],
    "dc:type": ["dc:type", "dcterms"],
    "dcterms:accessRights": ["dcterms:accessRights", "dcterms"],
    "dcterms:available": ["dcterms:available", "dcterms"],
    "dcterms:bibliographicCitation": ["dcterms:bibliographicCitation", "dcterms"],
    "dcterms:created": ["dcterms:created", "dcterms"],
    "dcterms:creator": ["dcterms:creator", "dcterms"],
    "dcterms:date": ["dcterms:date", "dcterms"],
    "dcterms:publisher": ["dcterms:publisher", "dcterms"],
    "dcterms:description": ["dcterms:description", "dcterms"],
    "dcterms:format": ["dcterms:format", "dcterms"],
    "dcterms:identifier": ["dcterms:identifier", "dcterms"],
    "dcterms:language": ["dcterms:language", "dcterms"],
    "dcterms:license": ["dcterms:license", "dcterms"],
    "dcterms:modified": ["dcterms:modified", "dcterms"],
    "dcterms:provider": ["dcterms:provider", "dcterms"],
    "dcterms:reference": ["dcterms:references", "dcterms"],
    "dcterms:references": ["dcterms:references", "dcterms"],
    "dcterms:rights": ["dcterms:rights", "dcterms"],
    "dcterms:rightsHolder": ["dcterms:rightsHolder", "dcterms"],
    "dcterms:source": ["dcterms:source", "dcterms"],
    "dcterms:spatial": ["dcterms:spatial", "dcterms"],
    "dcterms:subject": ["dcterms:subject", "dcterms"],
    "dcterms:temporal": ["dcterms:temporal", "dcterms"],
    "dcterms:title": ["dcterms:title", "dcterms"],
    "dcterms:type": ["dcterms:type", "dcterms"],
    "dcterms_modified": ["dcterms:modified", "dcterms"],
    "dcterms_rightsHolder": ["dcterms:rightsHolder", "dcterms"],
    "DecimalLatitude": ["dwc:decimalLatitude", "dwc:Occurrence"],
    "decimalLatitude": ["dwc:decimalLatitude", "dwc:Occurrence"],
    "decimalLongitude": ["dwc:decimalLongitude", "dwc:Occurrence"],
    "DecimalLongitude": ["dwc:decimalLongitude", "dwc:Occurrence"],
    "determination_history": ["idigbio:determinationHistory", "dwc:Occurrence"],
    "dwc: identificationQualifier": ["dwc:identificationQualifier", "dwc:Occurrence"],
    "dwc:acceptedNameUsage": ["dwc:acceptedNameUsage", "dwc:Occurrence"],
    "dwc:acceptedNameUsageID": ["dwc:acceptedNameUsageID", "dwc:Occurrence"],
    "dwc:accessRights": ["dwc:accessRights", "dwc:Occurrence"],
    "dwc:associatedMedia": ["dwc:associatedMedia", "dwc:Occurrence"],
    "dwc:associatedOccurrences": ["dwc:associatedOccurrences", "dwc:Occurrence"],
    "dwc:associatedReferences": ["dwc:associatedReferences", "dwc:Occurrence"],
    "dwc:associatedSequences": ["dwc:associatedSequences", "dwc:Occurrence"],
    "dwc:associatedTaxa": ["dwc:associatedTaxa", "dwc:Occurrence"],
    "dwc:basisOfRecord": ["dwc:basisOfRecord", "dwc:Occurrence"],
    "dwc:bed": ["dwc:bed", "dwc:Occurrence"],
    "dwc:behavior": ["dwc:behavior", "dwc:Occurrence"],
    "dwc:catalogNumber": ["dwc:catalogNumber", "dwc:Occurrence"],
    "dwc:class": ["dwc:class", "dwc:Occurrence"],
    "dwc:collectionCode": ["dwc:collectionCode", "dwc:Occurrence"],
    "dwc:collectionID": ["dwc:collectionID", "dwc:Occurrence"],
    "dwc:continent": ["dwc:continent", "dwc:Occurrence"],
    "dwc:coordinatePrecision": ["dwc:coordinatePrecision", "dwc:Occurrence"],
    "dwc:coordinateUncertaintyInMeters": ["dwc:coordinateUncertaintyInMeters", "dwc:Occurrence"],
    "dwc:country": ["dwc:country", "dwc:Occurrence"],
    "dwc:countryCode": ["dwc:countryCode", "dwc:Occurrence"],
    "dwc:county": ["dwc:county", "dwc:Occurrence"],
    "dwc:dataGeneralizations": ["dwc:dataGeneralizations", "dwc:Occurrence"],
    "dwc:datasetID": ["dwc:datasetID", "dwc:Occurrence"],
    "dwc:datasetName": ["dwc:datasetName", "dwc:Occurrence"],
    "dwc:dateIdentified": ["dwc:dateIdentified", "dwc:Occurence"],
    "dwc:day": ["dwc:day", "dwc:Occurrence"],
    "dwc:decimalLatitude": ["dwc:decimalLatitude", "dwc:Occurrence"],
    "dwc:decimalLongitude": ["dwc:decimalLongitude", "dwc:Occurrence"],
    "dwc:disposition": ["dwc:disposition", "dwc:Occurrence"],
    "dwc:dynamicProperties": ["dwc:dynamicProperties", "dwc:Occurrence"],
    "dwc:earliestAgeOrLowestStage": ["dwc:earliestAgeOrLowestStage", "dwc:Occurrence"],
    "dwc:earliestEonOrLowestEonothem": ["dwc:earliestEonOrLowestEonothem", "dwc:Occurrence"],
    "dwc:earliestEpochOrLowestSeries": ["dwc:earliestEpochOrLowestSeries", "dwc:Occurrence"],
    "dwc:earliestEraOrLowestErathem": ["dwc:earliestEraOrLowestErathem", "dwc:Occurrence"],
    "dwc:earliestPeriodOrLowestSystem": ["dwc:earliestPeriodOrLowestSystem", "dwc:Occurrence"],
    "dwc:endDayOfYear": ["dwc:endDayOfYear", "dwc:Occurrence"],
    "dwc:establishmentMeans": ["dwc:establishmentMeans", "dwc:Occurrence"],
    "dwc:eventDate": ["dwc:eventDate", "dwc:Occurrence"],
    "dwc:eventID": ["dwc:eventID", "dwc:Occurrence"],
    "dwc:eventRemarks": ["dwc:eventRemarks", "dwc:Occurrence"],
    "dwc:eventTime": ["dwc:eventTime", "dwc:Occurrence"],
    "dwc:family": ["dwc:family", "dwc:Occurrence"],
    "dwc:fieldNotes": ["dwc:fieldNotes", "dwc:Occurrence"],
    "dwc:fieldNumber": ["dwc:fieldNumber", "dwc:Occurrence"],
    "dwc:footprintSpatialFit": ["dwc:footprintSpatialFit", "dwc:Occurrence"],
    "dwc:footprintSRS": ["dwc:footprintSRS", "dwc:Occurrence"],
    "dwc:footprintWKT": ["dwc:footprintWKT", "dwc:Occurrence"],
    "dwc:formation": ["dwc:formation", "dwc:Occurrence"],
    "dwc:genus": ["dwc:genus", "dwc:Occurrence"],
    "dwc:geodeticDatum": ["dwc:geodeticDatum", "dwc:Occurrence"],
    "dwc:geologicalContextID": ["dwc:geologicalContextID", "dwc:Occurrence"],
    "dwc:georeferencedBy": ["dwc:georeferencedBy", "dwc:Occurrence"],
    "dwc:georeferencedDate": ["dwc:georeferencedDate", "dwc:Occurrence"],
    "dwc:georeferenceProtocol": ["dwc:georeferenceProtocol", "dwc:Occurrence"],
    "dwc:georeferenceRemarks": ["dwc:georeferenceRemarks", "dwc:Occurrence"],
    "dwc:georeferenceSources": ["dwc:georeferenceSources", "dwc:Occurrence"],
    "dwc:georeferenceVerificationStatus": ["dwc:georeferenceVerificationStatus", "dwc:Occurrence"],
    "dwc:group": ["dwc:group", "dwc:Occurrence"],
    "dwc:habitat": ["dwc:habitat", "dwc:Occurrence"],
    "dwc:higherClassification": ["dwc:higherClassification", "dwc:Occurrence"],
    "dwc:higherGeography": ["dwc:higherGeography", "dwc:Occurrence"],
    "dwc:higherGeographyID": ["dwc:higherGeographyID", "dwc:Occurrence"],
    "dwc:highestBiostratigraphicZone": ["dwc:highestBiostratigraphicZone", "dwc:Occurrence"],
    "dwc:identificationID": ["dwc:identificationID", "dwc:Occurrence"],
    "dwc:identificationQualifier": ["dwc:identificationQualifier", "dwc:Occurence"],
    "dwc:identificationReferences": ["dwc:identificationReferences", "dwc:Occurrence"],
    "dwc:identificationRemarks": ["dwc:identificationRemarks", "dwc:Occurrence"],
    "dwc:identificationVerificationStatus": ["dwc:identificationVerificationStatus", "dwc:Occurrence"],
    "dwc:identifiedBy": ["dwc:identifiedBy", "dwc:Occurence"],
    "dwc:individualCount": ["dwc:individualCount", "dwc:Occurrence"],
    "dwc:individualID": ["dwc:individualID", "dwc:Occurrence"],
    "dwc:informationWithheld": ["dwc:informationWithheld", "dwc:Occurrence"],
    "dwc:infraspecificEpithet": ["dwc:infraspecificEpithet", "dwc:Occurrence"],
    "dwc:institutionCode": ["dwc:institutionCode", "dwc:Occurrence"],
    "dwc:institutionID": ["dwc:institutionID", "dwc:Occurrence"],
    "dwc:island": ["dwc:island", "dwc:Occurrence"],
    "dwc:islandGroup": ["dwc:islandGroup", "dwc:Occurrence"],
    "dwc:kingdom": ["dwc:kingdom", "dwc:Occurrence"],
    "dwc:latestAgeOrHighestStage": ["dwc:latestAgeOrHighestStage", "dwc:Occurrence"],
    "dwc:latestEonOrHighestEonothem": ["dwc:latestEonOrHighestEonothem", "dwc:Occurrence"],
    "dwc:latestEpochOrHighestSeries": ["dwc:latestEpochOrHighestSeries", "dwc:Occurrence"],
    "dwc:latestEraOrHighestErathem": ["dwc:latestEraOrHighestErathem", "dwc:Occurrence"],
    "dwc:latestPeriodOrHighestSystem": ["dwc:latestPeriodOrHighestSystem", "dwc:Occurrence"],
    "dwc:lifeStage": ["dwc:lifeStage", "dwc:Occurence"],
    "dwc:lithostratigraphicTerms": ["dwc:lithostratigraphicTerms", "dwc:Occurrence"],
    "dwc:locality": ["dwc:locality", "dwc:Occurrence"],
    "dwc:locationAccordingTo": ["dwc:locationAccordingTo", "dwc:Occurrence"],
    "dwc:locationID": ["dwc:locationID", "dwc:Occurrence"],
    "dwc:locationRemarks": ["dwc:locationRemarks", "dwc:Occurrence"],
    "dwc:lowestBiostratigraphicZone": ["dwc:lowestBiostratigraphicZone", "dwc:Occurrence"],
    "dwc:maximumDepthInMeters": ["dwc:maximumDepthInMeters", "dwc:Occurrence"],
    "dwc:maximumDistanceAboveSurfaceInMeters": ["dwc:maximumDistanceAboveSurfaceInMeters", "dwc:Occurrence"],
    "dwc:maximumElevationInMeters": ["dwc:maximumElevationInMeters", "dwc:Occurrence"],
    "dwc:measurementRemarks": ["dwc:measurementRemarks", "dwc:MeasurementOrFact"],
    "dwc:measurementType": ["dwc:measurementType", "dwc:MeasurementOrFact"],
    "dwc:measurementUnit": ["dwc:measurementUnit", "dwc:MeasurementOrFact"],
    "dwc:measurementValue": ["dwc:measurementValue", "dwc:MeasurementOrFact"],
    "dwc:member": ["dwc:member", "dwc:Occurrence"],
    "dwc:minimumDepthInMeters": ["dwc:minimumDepthInMeters", "dwc:Occurrence"],
    "dwc:minimumDistanceAboveSurfaceInMeters": ["dwc:minimumDistanceAboveSurfaceInMeters", "dwc:Occurrence"],
    "dwc:minimumElevationInMeters": ["dwc:minimumElevationInMeters", "dwc:Occurrence"],
    "dwc:month": ["dwc:month", "dwc:Occurrence"],
    "dwc:municipality": ["dwc:municipality", "dwc:Occurrence"],
    "dwc:nameAccordingTo": ["dwc:nameAccordingTo", "dwc:Occurence"],
    "dwc:nameAccordingToID": ["dwc:nameAccordingToID", "dwc:Occurrence"],
    "dwc:namePublishedIn": ["dwc:namePublishedIn", "dwc:Occurrence"],
    "dwc:namePublishedInID": ["dwc:namePublishedInID", "dwc:Occurrence"],
    "dwc:namePublishedInYear": ["dwc:namePublishedInYear", "dwc:Occurrence"],
    "dwc:nomenclaturalCode": ["dwc:nomenclaturalCode", "dwc:Occurrence"],
    "dwc:nomenclaturalStatus": ["dwc:nomenclaturalStatus", "dwc:Occurrence"],
    "dwc:occurrenceID": ["dwc:occurrenceID", "dwc:Occurrence"],
    "dwc:occurrenceRemarks": ["dwc:occurrenceRemarks", "dwc:Occurrence"],
    "dwc:occurrenceStatus": ["dwc:occurrenceStatus", "dwc:Occurrence"],
    "dwc:order": ["dwc:order", "dwc:Occurrence"],
    "dwc:originalNameUsage": ["dwc:originalNameUsage", "dwc:Occurrence"],
    "dwc:originalNameUsageID": ["dwc:originalNameUsageID", "dwc:Occurrence"],
    "dwc:otherCatalogNumbers": ["dwc:otherCatalogNumbers", "dwc:Occurrence"],
    "dwc:ownerInstitutionCode": ["dwc:ownerInstitutionCode", "dwc:Occurrence"],
    "dwc:parentNameUsage": ["dwc:parentNameUsage", "dwc:Occurrence"],
    "dwc:parentNameUsageID": ["dwc:parentNameUsageID", "dwc:Occurrence"],
    "dwc:phylum": ["dwc:phylum", "dwc:Occurrence"],
    "dwc:pointRadiusSpatialFit": ["dwc:pointRadiusSpatialFit", "dwc:Occurrence"],
    "dwc:preparation": ["dwc:preparation", "dwc:Occurrence"],
    "dwc:preparations": ["dwc:preparations", "dwc:Occurence"],
    "dwc:previousIdentifications": ["dwc:previousIdentifications", "dwc:Occurrence"],
    "dwc:recordedBy": ["dwc:recordedBy", "dwc:Occurrence"],
    "dwc:recordNumber": ["dwc:recordNumber", "dwc:Occurrence"],
    "dwc:relatedResourceID": ["dwc:relatedResourceID", "dwc:ResourceRelationship"],
    "dwc:relationshipOfResource": ["dwc:relationshipOfResource", "dwc:ResourceRelationship"],
    "dwc:reproductiveCondition": ["dwc:reproductiveCondition", "dwc:Occurrence"],
    "dwc:rights": ["dwc:rights", "dwc:Occurrence"],
    "dwc:rightsHolder": ["dwc:rightsHolder", "dwc:Occurrence"],
    "dwc:samplingEffort": ["dwc:samplingEffort", "dwc:Occurrence"],
    "dwc:samplingProtocol": ["dwc:samplingProtocol", "dwc:Occurrence"],
    "dwc:scientificName": ["dwc:scientificName", "dwc:Occurence"],
    "dwc:scientificNameAuthorship": ["dwc:scientificNameAuthorship", "dwc:Occurrence"],
    "dwc:scientificNameID": ["dwc:scientificNameID", "dwc:Occurence"],
    "dwc:sex": ["dwc:sex", "dwc:Occurence"],
    "dwc:specificEpithet": ["dwc:specificEpithet", "dwc:Occurrence"],
    "dwc:startDayOfYear": ["dwc:startDayOfYear", "dwc:Occurrence"],
    "dwc:state": ["dwc:state", "dwc:Occurrence"],
    "dwc:stateProvince": ["dwc:stateProvince", "dwc:Occurrence"],
    "dwc:subgenus": ["dwc:subgenus", "dwc:Occurrence"],
    "dwc:taxonConceptID": ["dwc:taxonConceptID", "dwc:Occurrence"],
    "dwc:taxonID": ["dwc:taxonID", "dwc:Occurrence"],
    "dwc:taxonomicStatus": ["dwc:taxonomicStatus", "dwc:Occurrence"],
    "dwc:taxonRank": ["dwc:taxonRank", "dwc:Occurrence"],
    "dwc:taxonRemarks": ["dwc:taxonRemarks", "dwc:Occurrence"],
    "dwc:typeStatus": ["dwc:typeStatus", "dwc:Occurrence"],
    "dwc:verbatimCoordinates": ["dwc:verbatimCoordinates", "dwc:Occurrence"],
    "dwc:verbatimCoordinateSystem": ["dwc:verbatimCoordinateSystem", "dwc:Occurrence"],
    "dwc:verbatimDepth": ["dwc:verbatimDepth", "dwc:Occurrence"],
    "dwc:verbatimElevation": ["dwc:verbatimElevation", "dwc:Occurrence"],
    "dwc:VerbatimEventDate": ["dwc:verbatimEventDate", "dwc:Occurrence"],
    "dwc:verbatimEventDate": ["dwc:verbatimEventDate", "dwc:Occurrence"],
    "dwc:verbatimLatitude": ["dwc:verbatimLatitude", "dwc:Occurrence"],
    "dwc:verbatimLocality": ["dwc:verbatimLocality", "dwc:Occurrence"],
    "dwc:verbatimLongitude": ["dwc:verbatimLongitude", "dwc:Occurrence"],
    "dwc:verbatimSRS": ["dwc:verbatimSRS", "dwc:Occurrence"],
    "dwc:verbatimTaxonRank": ["dwc:verbatimTaxonRank", "dwc:Occurrence"],
    "dwc:vernacularName": ["dwc:vernacularName", "dwc:Occurence"],
    "dwc:waterBody": ["dwc:waterBody", "dwc:Occurrence"],
    "dwc:year": ["dwc:year", "dwc:Occurrence"],
    "dwc_associatedTaxa": ["dwc:associatedTaxa", "dwc:Occurrence"],
    "dwc_basisOfRecord": ["dwc:basisOfRecord", "dwc:Occurrence"],
    "dwc_class": ["dwc:class", "dwc:Occurrence"],
    "dwc_coordinateUncertaintyInMeters": ["dwc:coordinateUncertaintyInMeters", "dwc:Occurrence"],
    "dwc_country": ["dwc:country", "dwc:Occurrence"],
    "dwc_county": ["dwc:county", "dwc:Occurrence"],
    "dwc_datasetName": ["dwc:datasetName", "dwc:Occurrence"],
    "dwc_dateIdentified": ["dwc:dateIdentified", "dwc:Occurrence"],
    "dwc_decimalLatitude": ["dwc:decimalLatitude", "dwc:Occurrence"],
    "dwc_decimalLongitude": ["dwc:decimalLongitude", "dwc:Occurrence"],
    "dwc_eventDate": ["dwc:eventDate", "dwc:Occurrence"],
    "dwc_family": ["dwc:family", "dwc:Occurrence"],
    "dwc_genus": ["dwc:genus", "dwc:Occurrence"],
    "dwc_georeferenceRemarks": ["dwc:georeferenceRemarks", "dwc:Occurrence"],
    "dwc_higherClassification": ["dwc:higherClassification", "dwc:Occurrence"],
    "dwc_identifiedBy": ["dwc:identifiedBy", "dwc:Occurrence"],
    "dwc_individualCount": ["dwc:individualCount", "dwc:Occurrence"],
    "dwc_infraspecificEpithet": ["dwc:infraspecificEpithet", "dwc:Occurrence"],
    "dwc_kingdom": ["dwc:kingdom", "dwc:Occurrence"],
    "dwc_lifeStage": ["dwc:lifeStage", "dwc:Occurrence"],
    "dwc_locality": ["dwc:locality", "dwc:Occurrence"],
    "dwc_locationAccordingTo": ["dwc:locationAccordingTo", "dwc:Occurrence"],
    "dwc_occurrenceID": ["dwc:occurrenceID", "dwc:Occurrence"],
    "dwc_order": ["dwc:order", "dwc:Occurrence"],
    "dwc_otherCatalogNumbers": ["dwc:otherCatalogNumbers", "dwc:Occurrence"],
    "dwc_ownerInstitutionCode": ["dwc:ownerInstitutionCode", "dwc:Occurrence"],
    "dwc_phylum": ["dwc:phylum", "dwc:Occurrence"],
    "dwc_samplingProtocol": ["dwc:samplingProtocol", "dwc:Occurrence"],
    "dwc_scientificNameAuthorship": ["dwc:scientificNameAuthorship", "dwc:Occurrence"],
    "dwc_sex": ["dwc:sex", "dwc:Occurrence"],
    "dwc_specificEpithet": ["dwc:specificEpithet", "dwc:Occurrence"],
    "dwc_stateProvince": ["dwc:stateProvince", "dwc:Occurrence"],
    "dwc_typeStatus": ["dwc:typeStatus", "dwc:Occurrence"],
    "dwc_verbatimElevation": ["dwc:verbatimElevation", "dwc:Occurrence"],
    "dwc_verbatimEventDate": ["dwc:verbatimEventDate", "dwc:Occurrence"],
    "dwc_year": ["dwc:year", "dwc:Occurrence"],
    "earliestEpochOrLowestSeries": ["dwc:earliestEpochOrLowestSeries", "dwc:Occurrence"],
    "earliestEraOrLowestErathem": ["dwc:earliestEraOrLowestErathem", "dwc:Occurrence"],
    "earliestPeriodOrLowestSystem": ["dwc:earliestPeriodOrLowestSystem", "dwc:Occurrence"],
    "EndangeredStatus": ["inhs:EndangeredStatus", "dwc:Occurrence"],
    "Error": [None, "dwc:Multimedia"],
    "exif:PixelXDimension": ["exif:PixelXDimension", "dwc:Multimedia"],
    "exif:PixelYDimension": ["exif:PixelYDimension", "dwc:Multimedia"],
    "family": ["dwc:family", "dwc:Occurrence"],
    "fieldNumber": ["dwc:fieldNumber", "dwc:Occurrence"],
    "formation": ["dwc:formation", "dwc:Occurrence"],
    "gbif:canonicalName": ["gbif:canonicalName", "gbif:Taxon"],
    "gbif:isExtinct": ["gbif:isExtinct", "gbif:SpeciesProfile"],
    "gbif:isHybrid": ["gbif:isHybrid", "gbif:SpeciesProfile"],
    "gbif:isMarine": ["gbif:isMarine", "gbif:SpeciesProfile"],
    "gbif:isTerrestrial": ["gbif:isTerrestrial", "gbif:SpeciesProfile"],
    "gbif:typeDesignatedBy": ["gbif:typeDesignatedBy", "gbif:Taxon"],
    "gbif:typeDesignationType": ["gbif:typeDesignationType", "gbif:Taxon"],
    "gbif:verbatimLabel": ["gbif:verbatimLabel", "gbif:TypesAndSpecimen"],
    "genus": ["dwc:genus", "dwc:Occurrence"],
    "Genus": ["dwc:genus", "dwc:Occurrence"],
    "GeodeticDatum": ["dwc:geodeticDatum", "dwc:Occurrence"],
    "GeoreferenceProtocol": ["dwc:georeferenceProtocol", "dwc:Occurrence"],
    "GeoreferenceRemarks": ["dwc:georeferenceRemarks", "dwc:Occurrence"],
    "group": ["dwc:group", "dwc:Occurrence"],
    "host_family": ["idigbio:hostFamily", "dwc:Occurrence"],
    "id": ["id", "dwc:Text:Core"],
    "identifiedBy": ["dwc:identifiedBy", "dwc:Occurrence"],
    "idigbio:associatedFamily": ["idigbio:associatedFamily", "dwc:Occurrence"],
    "idigbio:associatedRecordReference": ["idigbio:associatedRecordReference", "dwc:Multimedia"],
    "idigbio:associatedRecordsetReference": ["idigbio:associatedRecordsetReference", "dwc:Multimedia"],
    "idigbio:associatedRelationship": ["idigbio:associatedRelationship", "dwc:Occurrence"],
    "idigbio:endangeredStatus": ["idigbio:endangeredStatus", "dwc:Occurrence"],
    "idigbio:preparationCount": ["idigbio:preparationCount", "dwc:Occurrence"],
    "idigbio:recordID": ["idigbio:recordId", "idigbio:Record"],
    "idigbio:recordId": ["idigbio:recordId", "idigbio:Record"],
    "idigbio:verbatimDateIdentified": ["idigbio:verbatimDateIdentified", "dwc:Occurrence"],
    "idigbio:substrate": ["idigbio:substrate", "dwc:Occurrence"],
    "idigbio_barcodeValue": ["idigbio:barcodeValue", "dwc:Occurrence"],
    "idigbio_recordID": ["idigbio:recordId", "idigbio:Record"],
    "iDigbioProvidedByGUID": ["idigbio:associatedRecordsetReference", "dwc:Multimedia"],
    "ImageURL": ["dwc:associatedMedia", "dwc:Occurrence"],
    "IndividualCount": ["dwc:individualCount", "dwc:Occurrence"],
    "individualCount": ["dwc:individualCount", "dwc:Occurrence"],
    "inhs:Dead": ["inhs:dead", "dwc:Occurrence"],
    "inhs:FormI_males": ["inhs:formI_males", "dwc:Occurrence"],
    "inhs:FormII_females": ["inhs:formII_females", "dwc:Occurrence"],
    "inhs:FormII_males": ["inhs:formII_males", "dwc:Occurrence"],
    "inhs:Instars_Female": ["inhs:instars_Female", "dwc:Occurrence"],
    "inhs:Instars_Male": ["inhs:instars_Male", "dwc:Occurrence"],
    "inhs:Juv_females": ["inhs:juv_females", "dwc:Occurrence"],
    "inhs:Juv_males": ["inhs:juv_males", "dwc:Occurrence"],
    "inhs:Juv_undetermined": ["inhs:juv_undetermined", "dwc:Occurrence"],
    "inhs:Live": ["inhs:live", "dwc:Occurrence"],
    "inhs:location_Basin": ["inhs:location_Basin", "dwc:Occurrence"],
    "inhs:location_RiverMile": ["inhs:location_RiverMile", "dwc:Occurrence"],
    "inhs:location_Stream": ["inhs:location_Stream", "dwc:Occurrence"],
    "inhs:locationTrs": ["inhs:locationTrs", "dwc:Occurrence"],
    "inhs:Relic": ["inhs:relic", "dwc:Occurrence"],
    "inhs:superfamily": ["idigbio:superfamily", "dwc:Occurrence"],
    "inhs:Total_females": ["inhs:total_females", "dwc:Occurrence"],
    "inhs:Total_Males": ["inhs:total_Males", "dwc:Occurrence"],
    "inhs:Vouchered": ["inhs:vouchered", "dwc:Occurrence"],
    "InstitutionCode": ["dwc:institutionCode", "dwc:Occurrence"],
    "institutionCode": ["dwc:institutionCode", "dwc:Occurrence"],
    "Iptc4xmpExt:City": ["Iptc4xmpExt:City", "dwc:Multimedia"],
    "Iptc4xmpExt:CreditLine": ["Iptc4xmpExt:CreditLine", "dwc:Multimedia"],
    "Iptc4xmpExt:CountryCode": ["Iptc4xmpExt:CountryCode", "dwc:Multimedia"],
    "Iptc4xmpExt:CountryName": ["Iptc4xmpExt:CountryName", "dwc:Multimedia"],
    "Iptc4xmpExt:CVterm": ["Iptc4xmpExt:CVterm", "dwc:Multimedia"],
    "Iptc4xmpExt:LocationCreated": ["Iptc4xmpExt:LocationCreated", "dwc:Multimedia"],
    "Iptc4xmpExt:LocationShown": ["Iptc4xmpExt:LocationShown", "dwc:Multimedia"],
    "Iptc4xmpExt:ProvinceState": ["Iptc4xmpExt:ProvinceState", "dwc:Multimedia"],
    "Iptc4xmpExt:Sublocation": ["Iptc4xmpExt:Sublocation", "dwc:Multimedia"],
    "Iptc4xmpExt:WorldRegion": ["Iptc4xmpExt:WorldRegion", "dwc:Multimedia"],
    "iucn:threatStatus": ["iucn:threatStatus", "gbif:Distribution"],
    "Locality": ["dwc:locality", "dwc:Occurrence"],
    "locality": ["dwc:locality", "dwc:Occurrence"],
    "location_Basin": ["inhs:locationBasin", "dwc:Occurrence"],
    "location_Stream": ["inhs:locationStream", "dwc:Occurrence"],
    "locationID": ["dwc:locationID", "dwc:Occurrence"],
    "locationRemarks": ["dwc:locationRemarks", "dwc:Occurrence"],
    "locationTrs": ["inhs:locationTrs", "dwc:Occurrence"],
    "lowestBiostratigraphicZone": ["dwc:lowestBiostratigraphicZone", "dwc:Occurrence"],
    "MediaEXIF": [None, "dwc:Multimedia"],
    "MediaGUID": ["idigbio:recordId", "dwc:Multimedia"],
    "MediaMD5": ["ac:hashValue", "dwc:Multimedia"],
    "MediaRecordEtag": [None, "dwc:Multimedia"],
    "MediaSizeInBytes": [None, "dwc:Multimedia"],
    "MediaURL": ["ac:accessURI", "dwc:Multimedia"],
    "member": ["dwc:member", "dwc:Occurrence"],
    "MimeType": ["dcterms:format", "dwc:Multimedia"],
    "modified": ["dcterms:modified", "dwc:Occurrence"],
    "Modified": ["dcterms:modified", "dwc:Occurrence"],
    "month": ["dwc:month", "dwc:Occurrence"],
    "MonthCollected": ["dwc:month", "dwc:Occurrence"],
    "Notes": ["dwc:occurrenceRemarks", "dwc:Occurrence"],
    "OccurrenceID": ["dwc:occurrenceID", "dwc:Occurrence"],
    "occurrenceID": ["dwc:occurrenceID", "dwc:Occurrence"],
    "occurrenceRemark": ["dwc:occurrenceRemarks", "dwc:Occurrence"],
    "occurrenceRemarks": ["dwc:occurrenceRemarks", "dwc:Occurrence"],
    "order": ["dwc:order", "dwc:Occurrence"],
    "Order": ["dwc:order", "dwc:Occurrence"],
    "OriginalFileName": [None, "dwc:Multimedia"],
    "photoshop:Credit": ["photoshop:Credit", "dwc:Multimedia"],
    "preparation": ["dwc:preparations", "dwc:Occurrence"],
    "preparationCount": ["inhs:preparationCount", "dwc:Occurrence"],
    "Preparations": ["dwc:preparations", "dwc:Occurrence"],
    "preparations": ["dwc:preparations", "dwc:Occurrence"],
    "providerCreatedByGUID": [None, "dwc:Multimedia"],
    "ProviderCreatedTimeStamp": [None, "dwc:Multimedia"],
    "recordedBy": ["dwc:recordedBy", "dwc:Occurrence"],
    "relatedRecourceID": ["dwc:relatedResourceID", "dwc:Occurrence"],
    "relatedResourceID": ["dwc:relatedResourceID", "dwc:Occurrence"],
    "RightsLicense": ["xmpRights:UsageTerms", "dwc:Multimedia"],
    "RightsLicenseLogoUrl": ["ac:licenseLogoURL", "dwc:Multimedia"],
    "RightsLicenseStatementUrl": ["xmpRights:WebStatement", "dwc:Multimedia"],
    "River_mile": ["inhs:riverMile", "dwc:Occurrence"],
    "SampleRemarks": ["dwc:eventRemarks", "dwc:Occurrence"],
    "scientificName": ["dwc:scientificName", "dwc:Occurrence"],
    "ScientificName": ["dwc:scientificName", "dwc:Occurrence"],
    "Sex": ["dwc:sex", "dwc:Occurrence"],
    "specificEpithet": ["dwc:specificEpithet", "dwc:Occurrence"],
    "SpecificEpithet": ["dwc:specificEpithet", "dwc:Occurrence"],
    "SpecimenUUID": ["idigbio:associatedRecordReference", "dwc:Multimedia"],
    "state": ["dwc:stateProvince", "dwc:Occurrence"],
    "StateProvince": ["dwc:stateProvince", "dwc:Occurrence"],
    "stateProvince": ["dwc:stateProvince", "dwc:Occurrence"],
    "fcc:superfamily": ["idigbio:superfamily", "dwc:Occurrence"],
    "fcc:subfamily": ["idigbio:subfamily", "dwc:Occurrence"],
    "fcc:datePicked": ["fcc:datePicked", "dwc:Occurrence"],
    "fcc:pickedBy": ["fcc:pickedBy", "dwc:Occurrence"],
    "idigbio:preservative": ["idigbio:preservative", "dwc:Occurrence"],
    "subfamily": ["idigbio:subfamily", "dwc:Occurrence"],
    "subgenus": ["idigbio:subgenus", "dwc:Occurrence"],
    "symbiota:verbatimScientificName": ["symbiota:verbatimScientificName", "symbiota:Record"],
    "symbiota:recordEnteredBy": ["symbiota:recordEnteredBy", "symbiota:Record"],
    "symbiota:identifiedByID": ["symbiota:identifiedByID", "symbiota:Record"],
    "symbiota:tidInterpreted": ["symbiota:tidInterpreted", "symbiota:Record"],
    "tribe": ["idigbio:tribe", "dwc:Occurrence"],
    "typeStatus": ["dwc:typeStatus", "dwc:Occurrence"],
    "UploadTime": ["dcterms:modified", "dwc:Multimedia"],
    "VerbatimCoordinateSystem": ["dwc:verbatimCoordinateSystem", "dwc:Occurrence"],
    "verbatimLocality": ["dwc:verbatimLocality", "dwc:Occurrence"],
    "VernacularName": ["dwc:vernacularName", "dwc:Occurrence"],
    "vernacularName": ["dwc:vernacularName", "dwc:Occurrence"],
    "Warnings": [None, "dwc:Multimedia"],
    "wgs84_pos:latitude": ["wgs84_pos:latitude", "dwc:Multimedia"],
    "wgs84_pos:longitude": ["wgs84_pos:longitude", "dwc:Multimedia"],
    "xmp:CreateDate": ["xmp:CreateDate", "dwc:Multimedia"],
    "xmp:MetadataDate": ["xmp:MetadataDate", "dwc:Multimedia"],
    "xmp:Rating": ["xmp:Rating", "dwc:Multimedia"],
    "xmpRights:Owner": ["xmpRights:Owner", "dwc:Multimedia"],
    "xmpRights:UsageTerms": ["xmpRights:UsageTerms", "dwc:Multimedia"],
    "xmpRights:WebStatement": ["xmpRights:WebStatement", "dwc:Multimedia"],
    "year": ["dwc:year", "dwc:Occurrence"],
    "YearCollected": ["dwc:year", "dwc:Occurrence"],
}

def get_types():
    return types

def get_canonical_name(f):
    # Remove all non-printable characters
    f = filter(lambda x: x in string.printable, f)
    if f in translate_dict:
        return translate_dict[f]
    else:
        # logger.warn("Unmapped field: \"{0}\"".format(f.encode("utf8")))
        return [f, "Unknown"]

def print_sorted_dict():
    ks = translate_dict.keys()
    ks = sorted(ks, key=lambda s: s.lower())
    print("{")
    for k in ks:
        print("    \"{0}\": {1},".format(k, json.dumps(translate_dict[k]).replace("null","None")))
    print("}")

def print_ns_counts():
    ks = translate_dict.keys()
    ks = sorted(ks, key=lambda s: s.lower())
    nsc = defaultdict(int)
    for k in ks:
        if translate_dict[k][0] is not None:
            ns = translate_dict[k][0].split(":")[0]
            if ns in namespaces_rev:
                nsc[namespaces_rev[ns]] += 1
    print(json.dumps(nsc,indent=2))

def get_short_term(f):
    for ns in sorted(namespaces.keys(),key=lambda x: len(x), reverse=True):
        if f.startswith(ns):
            return f.replace(ns,namespaces[ns]+":")
    print("NO NS: " + f)
    return f

def main():
    print_sorted_dict()
    print_ns_counts()

if __name__ == "__main__":
    main()
